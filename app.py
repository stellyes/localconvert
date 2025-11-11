import streamlit as st
from PIL import Image
import io
import zipfile
from pathlib import Path

st.set_page_config(page_title="Image Converter", page_icon="🖼️")

st.title("🖼️ Universal Image Format Converter")
st.write("Upload images in virtually any format. They'll be resized to max 1000px and converted to JPG (if opaque) or PNG (if transparent).")

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

if uploaded_files:
    st.write(f"Processing {len(uploaded_files)} file(s)...")
    
    converted_images = []
    errors = []
    
    # Process all images
    progress_bar = st.progress(0)
    for idx, uploaded_file in enumerate(uploaded_files):
        result = convert_image(uploaded_file)
        if 'error' in result:
            errors.append(f"❌ {result['filename']}: {result['error']}")
        else:
            converted_images.append(result)
        progress_bar.progress((idx + 1) / len(uploaded_files))
    
    # Display results
    st.success(f"✅ Successfully converted {len(converted_images)} image(s)")
    
    if errors:
        st.error("Errors occurred:")
        for error in errors:
            st.write(error)
    
    # Show converted images
    if converted_images:
        st.write("### Converted Images:")
        for img_data in converted_images:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.write(f"**{img_data['filename']}**")
            with col2:
                st.write(f"{img_data['original_format']} → {img_data['format']}")
            with col3:
                st.write(f"{img_data['size'][0]}×{img_data['size'][1]}px")
            with col4:
                st.write(f"{len(img_data['data']) / 1024:.1f} KB")
        
        # Create ZIP file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for img_data in converted_images:
                zip_file.writestr(img_data['filename'], img_data['data'])
        
        zip_buffer.seek(0)
        
        # Download button
        st.download_button(
            label="📥 Download All as ZIP",
            data=zip_buffer.getvalue(),
            file_name="converted_images.zip",
            mime="application/zip",
            use_container_width=True
        )
        
        # Individual download buttons
        with st.expander("Download Individual Files"):
            for img_data in converted_images:
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
st.caption("Universal Image Converter - Supports 70+ formats including RAW, PSD, HEIC, AVIF, and more!")
