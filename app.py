import streamlit as st
from PIL import Image
import io
import zipfile
from pathlib import Path

st.set_page_config(page_title="LocalConvert", page_icon="🖼️")

st.title("🖼️ Image Format Converter")
st.write("Upload images in any format. They'll be resized to max 1000px and converted to JPG (if opaque) or PNG (if transparent).")

# Supported formats
SUPPORTED_FORMATS = ['webp', 'gif', 'png', 'jpeg', 'jpg', 'jfif', 'tiff', 'bmp', 'svg', 'heif', 'avif', 'eps', 'heic']

uploaded_files = st.file_uploader(
    "Choose image files",
    type=SUPPORTED_FORMATS,
    accept_multiple_files=True
)

def has_transparency(img):
    """Check if image has transparency"""
    if img.mode in ('RGBA', 'LA', 'P'):
        if img.mode == 'P':
            # Check if palette has transparency
            if 'transparency' in img.info:
                return True
            # Convert to RGBA to check
            img = img.convert('RGBA')
        # Check alpha channel
        if img.mode in ('RGBA', 'LA'):
            alpha = img.getchannel('A')
            return alpha.getextrema()[0] < 255
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
        
        # Convert certain formats to RGB/RGBA first
        if img.mode in ('P', 'LA', 'L'):
            if has_transparency(img):
                img = img.convert('RGBA')
            else:
                img = img.convert('RGB')
        elif img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGB')
        
        # Resize
        img = resize_image(img)
        
        # Determine output format
        has_alpha = has_transparency(img)
        output_format = 'PNG' if has_alpha else 'JPEG'
        
        # Convert to appropriate mode
        if output_format == 'JPEG' and img.mode != 'RGB':
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
            'size': img.size
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
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{img_data['filename']}**")
            with col2:
                st.write(f"{img_data['format']}")
            with col3:
                st.write(f"{img_data['size'][0]}x{img_data['size'][1]}px")
        
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
            mime="application/zip"
        )
        
        # Individual download buttons
        with st.expander("Download Individual Files"):
            for img_data in converted_images:
                st.download_button(
                    label=f"Download {img_data['filename']}",
                    data=img_data['data'],
                    file_name=img_data['filename'],
                    mime=f"image/{img_data['format'].lower()}"
                )

else:
    st.info("👆 Upload some images to get started!")

# Footer
st.markdown("---")
st.caption("Supports: WEBP, GIF, PNG, JPEG, JPG, JFIF, TIFF, BMP, SVG, HEIF, AVIF, EPS, HEIC")
