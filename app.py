import streamlit as st
from PIL import Image
import io
import zipfile
from pathlib import Path
import cloudinary
import cloudinary.uploader
import cloudinary.api
import requests
import base64

st.set_page_config(page_title="LocalConvert", page_icon="🖼️")

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

# Configure Cloudinary
try:
    cloudinary.config(
        cloud_name=st.secrets.get("cloudinary_cloud_name", ""),
        api_key=st.secrets.get("cloudinary_api_key", ""),
        api_secret=st.secrets.get("cloudinary_api_secret", ""),
        secure=True
    )
    CLOUDINARY_CONFIGURED = bool(st.secrets.get("cloudinary_cloud_name"))
except Exception as e:
    CLOUDINARY_CONFIGURED = False

st.title("LocalConvert")
st.write("Upload images and choose to convert formats or upscale using AI.")

# Show system info
if CLOUDINARY_CONFIGURED:
    st.info("🚀 AI Upscaling: Cloudinary Generative AI (cloud-based)")
else:
    st.warning("⚠️ Cloudinary not configured. Add credentials to Streamlit secrets for AI upscaling. Using basic Lanczos upscaling instead.")

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

def upscale_image_cloudinary(uploaded_file, scale=2):
    """Upscale image using Cloudinary's AI upscaling"""
    try:
        # Read file bytes
        uploaded_file.seek(0)
        file_bytes = uploaded_file.read()
        uploaded_file.seek(0)
        
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            file_bytes,
            folder="streamlit_upscale",
            resource_type="image"
        )
        
        public_id = upload_result['public_id']
        
        # Get original dimensions
        original_width = upload_result['width']
        original_height = upload_result['height']
        
        # Calculate target dimensions
        target_width = original_width * scale
        target_height = original_height * scale
        
        # Generate upscaled URL with Cloudinary transformations
        upscaled_url = cloudinary.CloudinaryImage(public_id).build_url(
            effect="upscale",
            width=target_width,
            height=target_height,
            crop="scale",
            quality="auto:best"
        )
        
        # Download the upscaled image
        response = requests.get(upscaled_url, timeout=60)
        
        if response.status_code != 200:
            raise Exception(f"Failed to download upscaled image: {response.status_code}")
        
        # Open the upscaled image to get info
        img = Image.open(io.BytesIO(response.content))
        
        # Clean up - delete from Cloudinary
        try:
            cloudinary.uploader.destroy(public_id)
        except:
            pass  # Ignore cleanup errors
        
        # Generate filename
        original_name = Path(uploaded_file.name).stem
        new_filename = f"{original_name}_upscaled_{scale}x.png"
        
        return {
            'data': response.content,
            'filename': new_filename,
            'format': 'PNG',
            'size': img.size,
            'original_format': 'cloudinary_upscaled'
        }
    except Exception as e:
        return {'error': str(e), 'filename': uploaded_file.name}

def upscale_image_basic(uploaded_file, scale=2):
    """Basic upscaling using Lanczos resampling (fallback)"""
    try:
        # Open image
        img = Image.open(uploaded_file)
        
        # Convert to RGB if necessary
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGB')
        
        # Calculate new size
        new_width = img.width * scale
        new_height = img.height * scale
        
        # Upscale using high-quality Lanczos resampling
        output_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
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
            'original_format': 'upscaled_basic'
        }
    except Exception as e:
        return {'error': str(e), 'filename': uploaded_file.name}

if uploaded_files:
    st.write(f"### {len(uploaded_files)} file(s) uploaded")
    
    # Show operation selection
    st.write("### Choose an operation:")
    
    col1, col2 = st.columns(2)
    with col1:
        upscale_label = "AI Upscale (Cloudinary)" if CLOUDINARY_CONFIGURED else "Upscale (Lanczos)"
        operation = st.radio(
            "What would you like to do?",
            ["Convert & Resize", upscale_label],
            help="Convert: Optimize format and resize to 1000px max | Upscale: Enhance image size with AI"
        )
    
    if "Upscale" in operation:
        with col2:
            scale = st.selectbox(
                "Upscale factor",
                [2, 3, 4],
                index=0,
                help="Higher values = larger output files. Cloudinary AI works best at 2-4x."
            )
    
    # Process button
    if st.button("🚀 Process Images", type="primary", use_container_width=True):
        processed_images = []
        errors = []
        
        # Process all images
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Processing {uploaded_file.name}...")
            
            if operation == "Convert & Resize":
                result = convert_image(uploaded_file)
            else:  # Upscale
                if CLOUDINARY_CONFIGURED:
                    result = upscale_image_cloudinary(uploaded_file, scale)
                else:
                    result = upscale_image_basic(uploaded_file, scale)
            
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
                        method = "Cloudinary AI" if img_data['original_format'] == 'cloudinary_upscaled' else "Lanczos"
                        st.write(f"{method} {scale}x")
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
if CLOUDINARY_CONFIGURED:
    st.caption("AI Image Processor - Convert & Upscale | Powered by Cloudinary AI | Supports 70+ formats")
else:
    st.caption("Image Processor - Convert & Upscale | Basic Lanczos Upscaling | Supports 70+ formats")
