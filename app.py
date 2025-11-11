import streamlit as st
from PIL import Image
import io
import zipfile
from pathlib import Path
import sys

st.set_page_config(page_title="Image Processor", page_icon="🖼️")

# Password protection
def check_password():
    """Returns `True` if the user has entered the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets.get("app_password", "password"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    # First run, show input for password
    if "password_correct" not in st.session_state:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.write("*Please enter the password to access the app.*")
        return False
    # Password not correct, show input + error
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    # Password correct
    else:
        return True

if not check_password():
    st.stop()  # Don't continue if password check fails

# Check for Real-ESRGAN availability
try:
    import torch
    import numpy as np
    from basicsr.archs.rrdbnet_arch import RRDBNet
    from realesrgan import RealESRGANer
    REALESRGAN_AVAILABLE = True
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
except ImportError:
    REALESRGAN_AVAILABLE = False
    DEVICE = 'cpu'

st.title("🖼️ AI Image Processor")
st.write("Upload images and choose to convert formats or upscale using AI.")

# Show system info
if REALESRGAN_AVAILABLE:
    device_emoji = "🚀" if DEVICE == 'cuda' else "🐌"
    st.info(f"{device_emoji} AI Upscaling: {'GPU acceleration enabled' if DEVICE == 'cuda' else 'CPU mode (slower)'}")
else:
    st.warning("⚠️ AI Upscaling unavailable. Install with: `pip install realesrgan basicsr`")

# Comprehensive list of supported formats
SUPPORTED_FORMATS = [
    # Common raster formats
    'webp', 'gif', 'png', 'jpeg', 'jpg', 'jpe', 'jfif', 'jfi',
    # TIFF variants
    'tiff', 'tif',
    # Bitmap formats
    'bmp', 'dib',
    # JPEG 2000
    'jp2', 'j2k', 'jpf', 'jpx', 'jpm',
    # Raw formats
    'raw', 'dng', 'cr2', 'nef', 'arw', 'orf', 'rw2', 'pef', 'srw',
    # Vector formats
    'svg', 'svgz', 'eps', 'ps', 'pdf',
    # Modern formats
    'heif', 'heic', 'heics', 'avif', 'avifs',
    # Web formats
    'webp',
    # Photoshop
    'psd', 'psb',
    # Paint formats
    'pcx', 'ppm', 'pgm', 'pbm', 'pnm',
    # Targa
    'tga', 'icb', 'vda', 'vst',
    # SGI
    'sgi', 'rgb', 'bw',
    # Sun raster
    'ras',
    # Wireless bitmap
    'wbmp',
    # Windows formats
    'ico', 'cur',
    # FITS (astronomy)
    'fits', 'fit', 'fts',
    # Medical imaging
    'dcm', 'dicom',
    # HDR formats
    'hdr', 'pic', 'exr',
    # DDS (DirectDraw Surface)
    'dds',
    # FLIF
    'flif',
    # WebP animated
    'webp',
    # MNG
    'mng',
    # Additional
    'xbm', 'xpm', 'im', 'msp', 'palm', 'pcd', 'pixar', 'ppm', 'sgi', 'spider', 'wal', 'wmf', 'emf'
]

uploaded_files = st.file_uploader(
    "Choose image files",
    type=SUPPORTED_FORMATS,
    accept_multiple_files=True,
    help="Supports 70+ image formats including RAW, PSD, EPS, HEIC, and more!"
)

# Initialize Real-ESRGAN model (cached)
@st.cache_resource
def load_realesrgan_model(scale=4):
    """Load Real-ESRGAN model (cached)"""
    if not REALESRGAN_AVAILABLE:
        return None
    
    try:
        # Use RealESRGAN_x4plus model
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=scale)
        
        upsampler = RealESRGANer(
            scale=scale,
            model_path='https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth',
            model=model,
            tile=0,
            tile_pad=10,
            pre_pad=0,
            half=True if DEVICE == 'cuda' else False,
            device=DEVICE
        )
        return upsampler
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def has_transparency(img):
    """Check if image has transparency"""
    if img.mode in ('RGBA', 'LA', 'PA'):
        # Check alpha channel
        alpha = img.getchannel('A')
        return alpha.getextrema()[0] < 255
    elif img.mode == 'P':
        # Check if palette has transparency
        if 'transparency' in img.info:
            return True
        # Convert to RGBA to check
        try:
            img_rgba = img.convert('RGBA')
            alpha = img_rgba.getchannel('A')
            return alpha.getextrema()[0] < 255
        except:
            return False
    return False

def resize_image(img, max_size=1000):
    """Resize image maintaining aspect ratio"""
    width, height = img.size
    if width > max_size or height > max_size:
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))
        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return img

def convert_image(uploaded_file):
    """Convert and process a single image"""
    try:
        # Open image
        img = Image.open(uploaded_file)
        
        # Handle special cases for various formats
        original_mode = img.mode
        
        # Convert palette and indexed modes
        if img.mode in ('P', 'PA'):
            if has_transparency(img):
                img = img.convert('RGBA')
            else:
                img = img.convert('RGB')
        # Convert grayscale with alpha
        elif img.mode in ('LA', 'La'):
            if has_transparency(img):
                img = img.convert('RGBA')
            else:
                img = img.convert('RGB')
        # Convert simple grayscale
        elif img.mode in ('L', '1'):
            img = img.convert('RGB')
        # Convert CMYK (common in print files)
        elif img.mode == 'CMYK':
            img = img.convert('RGB')
        # Convert other exotic modes
        elif img.mode not in ('RGB', 'RGBA'):
            try:
                if 'A' in img.mode or has_transparency(img):
                    img = img.convert('RGBA')
                else:
                    img = img.convert('RGB')
            except:
                img = img.convert('RGB')
        
        # Resize
        img = resize_image(img)
        
        # Determine output format
        has_alpha = has_transparency(img)
        output_format = 'PNG' if has_alpha else 'JPEG'
        
        # Convert to appropriate mode for output
        if output_format == 'JPEG' and img.mode != 'RGB':
            img = img.convert('RGB')
        elif output_format == 'PNG' and img.mode not in ('RGB', 'RGBA'):
            if has_alpha:
                img = img.convert('RGBA')
            else:
                img = img.convert('RGB')
        
        # Save to bytes
        output = io.BytesIO()
        if output_format == 'JPEG':
            img.save(output, format='JPEG', quality=95, optimize=True)
            extension = '.jpg'
        else:
            img.save(output, format='PNG', optimize=True)
            extension = '.png'
        
        output.seek(0)
        
        # Generate filename
        original_name = Path(uploaded_file.name).stem
        new_filename = f"{original_name}{extension}"
        
        return {
            'data': output.getvalue(),
            'filename': new_filename,
            'format': output_format,
            'size': img.size,
            'original_format': original_mode
        }
    except Exception as e:
        return {'error': str(e), 'filename': uploaded_file.name}

def upscale_image_realesrgan(uploaded_file, upsampler, scale=4):
    """Upscale image using Real-ESRGAN"""
    try:
        # Open image
        img = Image.open(uploaded_file)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Convert to numpy array
        img_np = np.array(img)
        
        # Upscale using Real-ESRGAN
        output_np, _ = upsampler.enhance(img_np, outscale=scale)
        
        # Convert back to PIL Image
        output_img = Image.fromarray(output_np)
        
        # Save to bytes
        output = io.BytesIO()
        output_img.save(output, format='PNG', optimize=True)
        output.seek(0)
        
        # Generate filename
        original_name = Path(uploaded_file.name).stem
        new_filename = f"{original_name}_upscaled_{scale}x.png"
        
        return {
            'data': output.getvalue(),
            'filename': new_filename,
            'format': 'PNG',
            'size': output_img.size,
            'original_format': 'upscaled'
        }
    except Exception as e:
        return {'error': str(e), 'filename': uploaded_file.name}

if uploaded_files:
    st.write(f"### {len(uploaded_files)} file(s) uploaded")
    
    # Show operation selection
    st.write("### Choose an operation:")
    
    # Disable upscaling if not available
    if not REALESRGAN_AVAILABLE:
        operation = "Convert & Resize"
        st.info("📋 Only conversion available. Install Real-ESRGAN for AI upscaling.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            operation = st.radio(
                "What would you like to do?",
                ["Convert & Resize", "AI Upscale"],
                help="Convert: Optimize format and resize to 1000px max | Upscale: Enhance quality using Real-ESRGAN (local processing)"
            )
        
        if operation == "AI Upscale":
            with col2:
                scale = st.selectbox(
                    "Upscale factor",
                    [2, 4],
                    index=1,
                    help="Higher values = larger output files"
                )
    
    # Process button
    if st.button("🚀 Process Images", type="primary", use_container_width=True):
        processed_images = []
        errors = []
        
        # Load model if upscaling
        upsampler = None
        if operation == "AI Upscale" and REALESRGAN_AVAILABLE:
            with st.spinner("Loading AI model..."):
                upsampler = load_realesrgan_model(scale=scale if operation == "AI Upscale" else 4)
                if upsampler is None:
                    st.error("Failed to load Real-ESRGAN model. Please check installation.")
                    st.stop()
        
        # Process all images
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Processing {uploaded_file.name}...")
            
            if operation == "Convert & Resize":
                result = convert_image(uploaded_file)
            else:  # AI Upscale
                result = upscale_image_realesrgan(uploaded_file, upsampler, scale)
            
            if 'error' in result:
                errors.append(f"❌ {result['filename']}: {result['error']}")
            else:
                processed_images.append(result)
            
            progress_bar.progress((idx + 1) / len(uploaded_files))
        
        status_text.empty()
        
        # Display results
        if processed_images:
            st.success(f"✅ Successfully processed {len(processed_images)} image(s)")
        
        if errors:
            with st.expander("⚠️ Errors occurred", expanded=True):
                for error in errors:
                    st.write(error)
        
        # Show processed images
        if processed_images:
            st.write("### Processed Images:")
            for img_data in processed_images:
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    st.write(f"**{img_data['filename']}**")
                with col2:
                    if operation == "Convert & Resize":
                        st.write(f"{img_data['original_format']} → {img_data['format']}")
                    else:
                        st.write(f"Upscaled {scale}x")
                with col3:
                    st.write(f"{img_data['size'][0]}×{img_data['size'][1]}px")
                with col4:
                    st.write(f"{len(img_data['data']) / 1024:.1f} KB")
            
            # Create ZIP file
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for img_data in processed_images:
                    zip_file.writestr(img_data['filename'], img_data['data'])
            
            zip_buffer.seek(0)
            
            # Download button
            st.download_button(
                label="📥 Download All as ZIP",
                data=zip_buffer.getvalue(),
                file_name=f"processed_images_{operation.replace(' ', '_').lower()}.zip",
                mime="application/zip",
                use_container_width=True
            )
            
            # Individual download buttons
            with st.expander("Download Individual Files"):
                for img_data in processed_images:
                    st.download_button(
                        label=f"Download {img_data['filename']}",
                        data=img_data['data'],
                        file_name=img_data['filename'],
                        mime=f"image/{img_data['format'].lower()}",
                        key=img_data['filename']
                    )

else:
    st.info("👆 Upload some images to get started!")
    
    # Show supported formats in expandable section
    with st.expander("📋 View All Supported Formats (70+)"):
        st.write("**Common Formats:**")
        st.write("JPG/JPEG, PNG, GIF, WEBP, BMP, TIFF")
        
        st.write("**Modern Formats:**")
        st.write("HEIF/HEIC, AVIF")
        
        st.write("**Professional Formats:**")
        st.write("PSD (Photoshop), EPS, PDF, RAW files (CR2, NEF, ARW, DNG, etc.)")
        
        st.write("**JPEG 2000:**")
        st.write("JP2, J2K, JPF, JPX")
        
        st.write("**Specialized Formats:**")
        st.write("DICOM (medical), FITS (astronomy), HDR/EXR (high dynamic range), DDS (textures)")
        
        st.write("**Legacy Formats:**")
        st.write("PCX, TGA, SGI, Sun Raster, ICO, and many more")

# Footer
st.markdown("---")
st.caption("AI Image Processor - Convert & Upscale | Powered by Real-ESRGAN | Supports 70+ formats")
