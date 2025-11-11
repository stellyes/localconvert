# 🖼️ Universal Image Format Converter

A powerful, versatile web application built with Streamlit that converts images from 70+ formats to optimal web-friendly outputs while intelligently handling transparency and resizing.

## Features

### Universal Format Support
Convert from an extensive range of image formats including:
- **Common formats**: JPG, PNG, GIF, WEBP, BMP, TIFF
- **Modern formats**: HEIF/HEIC, AVIF
- **Professional formats**: PSD (Photoshop), EPS, PDF
- **RAW camera formats**: CR2, NEF, ARW, DNG, ORF, RW2, PEF, SRW, and more
- **JPEG 2000 variants**: JP2, J2K, JPF, JPX, JPM
- **Specialized formats**: DICOM (medical imaging), FITS (astronomy), HDR/EXR (high dynamic range), DDS (textures)
- **Legacy formats**: PCX, TGA, SGI, Sun Raster, ICO, and many others

Over 70 total formats supported!

### Smart Format Detection
The app automatically analyzes each image and converts it to the most appropriate format:
- **PNG** for images with transparency (alpha channels)
- **JPG** for opaque images (smaller file sizes)

### Intelligent Mode Conversion
Handles complex color modes seamlessly:
- CMYK to RGB (common in print files)
- Palette and indexed colors
- Grayscale with and without alpha
- Multiple transparency detection methods

### Automatic Resizing
All images are automatically resized to a maximum dimension of 1000 pixels (width or height) while maintaining their original aspect ratio. This ensures manageable file sizes without sacrificing quality.

### Batch Processing
Upload and convert multiple images simultaneously with a visual progress indicator showing real-time conversion status.

### Comprehensive File Information
View detailed information about each conversion:
- Original format → Output format
- Final dimensions
- File size in KB

### Flexible Download Options
- Download all converted images in a single ZIP file
- Download individual images separately
- Full-width download button for easy access

## Supported Input Formats

### Raster Formats
WEBP, GIF, PNG, JPEG, JPG, JPE, JFIF, JFI, TIFF, TIF, BMP, DIB, PCX, PPM, PGM, PBM, PNM, WBMP, XBM, XPM

### Modern Web Formats
HEIF, HEIC, HEICS, AVIF, AVIFS

### JPEG 2000 Family
JP2, J2K, JPF, JPX, JPM

### RAW Camera Formats
RAW, DNG, CR2 (Canon), NEF (Nikon), ARW (Sony), ORF (Olympus), RW2 (Panasonic), PEF (Pentax), SRW (Samsung)

### Professional Formats
PSD, PSB (Photoshop), EPS, PS (PostScript), PDF, SVG, SVGZ

### Graphics Formats
TGA, ICB, VDA, VST (Targa), SGI, RGB, BW (Silicon Graphics), ICO, CUR (Windows icons)

### Specialized Formats
DICOM, DCM (medical imaging), FITS, FIT, FTS (astronomy), HDR, PIC, EXR (high dynamic range), DDS (DirectDraw Surface textures), FLIF

### Additional Formats
RAS (Sun Raster), MNG, IM, MSP, PALM, PCD, PIXAR, SPIDER, WAL, WMF, EMF

## Security

### Password Protection

The app includes password protection to restrict access. The password is stored securely in Streamlit's secrets management system.

**Setting up the password:**

1. Create a `.streamlit/secrets.toml` file in your project directory:
```toml
app_password = "password"
```

2. For Streamlit Cloud deployment:
   - Go to your app settings
   - Navigate to "Secrets" section
   - Add: `app_password = "password"`

3. Change "password" to your desired password

**Important**: Never commit your `secrets.toml` file to version control. Add it to `.gitignore`:
```
.streamlit/secrets.toml
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Local Installation

1. Clone this repository or download the files:
```bash
git clone <your-repository-url>
cd image-converter
```

2. Create a `.streamlit` directory and `secrets.toml` file:
```bash
mkdir .streamlit
echo 'app_password = "password"' > .streamlit/secrets.toml
```

3. Add secrets to `.gitignore`:
```bash
echo '.streamlit/secrets.toml' >> .gitignore
```

4. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. For RAW format support, you may need to install additional system libraries:

**On Ubuntu/Debian:**
```bash
sudo apt-get install libraw-dev
pip install rawpy
```

**On macOS:**
```bash
brew install libraw
pip install rawpy
```

**On Windows:**
Download and install LibRaw from the official website, then:
```bash
pip install rawpy
```

4. Run the application:
```bash
streamlit run app.py
```

5. Enter the password when prompted (default: "password")

6. Open your browser and navigate to the local URL displayed in the terminal (typically `http://localhost:8501`)

## Deployment

### Deploy to Streamlit Cloud

1. Push your code to a GitHub repository with the following structure:
```
your-repo/
├── app.py
├── requirements.txt
└── README.md
```

2. Visit [share.streamlit.io](https://share.streamlit.io)

3. Sign in with your GitHub account

4. Click "New app"

5. Select your repository, branch, and main file (`app.py`)

6. **Important**: Before deploying, add the password to Secrets:
   - In your app dashboard, go to "Settings" → "Secrets"
   - Add the following:
   ```toml
   app_password = "password"
   ```
   - Change "password" to your desired password

7. Click "Deploy"

Your app will be live at `https://your-app-name.streamlit.app` within minutes!

**Note:** Some specialized formats (RAW, DICOM, FITS) may require additional system packages that aren't available on Streamlit Cloud by default. The app will still work with 60+ other formats.

### Deploy to Other Platforms

The app can also be deployed to:
- **Heroku**: Add a `Procfile` with `web: streamlit run app.py --server.port=$PORT` and include system dependencies in `Aptfile`
- **Google Cloud Run**: Containerize with Docker, including necessary system libraries
- **AWS EC2**: Run on a virtual machine with full control over system packages

## Usage

### Basic Workflow

1. **Upload Images**: Click the "Choose image files" button and select one or more images from your computer (supports 70+ formats!)

2. **Automatic Processing**: The app will:
   - Detect the original format and color mode
   - Analyze each image for transparency
   - Convert color modes appropriately (CMYK→RGB, grayscale, etc.)
   - Resize images to max 1000px dimension
   - Convert to PNG (if transparent) or JPG (if opaque)
   - Display detailed conversion results

3. **Review Results**: See a detailed breakdown showing:
   - Original format → Output format
   - Final dimensions in pixels
   - File size in kilobytes

4. **Download Results**:
   - Click "Download All as ZIP" for a single archive
   - Or expand "Download Individual Files" for separate downloads

### Example Use Cases

**Photography Workflow**: Batch convert RAW camera files (CR2, NEF, ARW) to web-friendly JPG format at 1000px for portfolio websites or social media.

**Professional Design**: Convert Photoshop PSD files or EPS vector graphics to optimized web formats while preserving transparency where needed.

**Medical Imaging**: Convert DICOM medical images to standard formats for presentations or documentation.

**Legacy File Recovery**: Convert old format images (PCX, TGA, SGI) to modern formats for archival or usage.

**Logo and Graphics**: Convert logos in various formats with transparency to optimized PNG files while maintaining quality and reducing file size.

**Mixed Media Projects**: Upload various format types from different sources and let the app intelligently choose the best output format based on each image's characteristics.

## Technical Details

### Image Processing Pipeline

The application follows this enhanced processing sequence for each uploaded image:

1. **Format Detection**: Opens the image and identifies its current format and color mode
2. **Mode Analysis**: Determines if special handling is needed (CMYK, palette, grayscale, etc.)
3. **Transparency Check**: Analyzes alpha channels and palette transparency across multiple modes
4. **Intelligent Conversion**: Converts to RGBA (if transparent) or RGB (if opaque) with special handling for:
   - CMYK color space (common in print files)
   - Palette and indexed colors
   - Grayscale variants (L, LA, 1)
   - Exotic color modes
5. **Resizing**: Scales image to max 1000px using high-quality Lanczos resampling
6. **Output Selection**: Chooses PNG or JPG based on transparency detection
7. **Final Conversion**: Ensures output mode matches format requirements
8. **Optimization**: Applies format-specific optimization (JPG quality: 95%, PNG: optimized)
9. **Packaging**: Collects all converted images with detailed metadata for download

### Color Mode Handling

The app intelligently handles various color modes:
- **CMYK**: Common in print files, converted to RGB for web use
- **Palette (P, PA)**: Indexed colors with optional transparency
- **Grayscale (L, LA, 1)**: Single-channel images with optional alpha
- **RGB/RGBA**: Standard color modes (passed through or alpha-stripped)
- **Exotic modes**: Fallback conversion with transparency preservation

### Quality Settings

- **JPEG Quality**: 95% (excellent quality with reasonable compression)
- **PNG Optimization**: Enabled (reduces file size without quality loss)
- **Resampling Method**: Lanczos (highest quality resizing algorithm)

### Transparency Detection

The app checks for transparency through multiple robust methods:
- Direct alpha channel analysis in RGBA, LA, and PA modes
- Palette transparency detection in indexed color (P mode)
- Safe conversion testing for ambiguous formats
- Alpha channel extrema checking to verify actual transparency usage

## Dependencies

```
streamlit - Web application framework
pillow - Image processing library (supports 40+ formats natively)
```

Optional for extended format support:
```
rawpy - RAW camera format support
pydicom - DICOM medical imaging support
astropy - FITS astronomy format support
OpenEXR - HDR/EXR format support
```

Full version specifications are available in `requirements.txt`.

## Troubleshooting

### Common Issues

**Issue**: "Module not found" error when running
**Solution**: Ensure all dependencies are installed with `pip install -r requirements.txt`

**Issue**: RAW formats (CR2, NEF, etc.) not uploading or converting
**Solution**: Install `rawpy` and system LibRaw library. See installation instructions above.

**Issue**: DICOM files not processing
**Solution**: Install `pydicom` with `pip install pydicom`

**Issue**: Some exotic formats showing errors
**Solution**: Certain formats may require additional system libraries. Check Pillow documentation for specific format requirements.

**Issue**: EPS or PDF files not converting properly
**Solution**: These vector formats require Ghostscript installed on your system:
- Ubuntu/Debian: `sudo apt-get install ghostscript`
- macOS: `brew install ghostscript`
- Windows: Download from ghostscript.com

**Issue**: Large RAW images causing slow processing
**Solution**: This is expected behavior for RAW files which are very large. Processing may take 10-30 seconds per image.

**Issue**: CMYK JPEGs appearing with incorrect colors
**Solution**: The app automatically converts CMYK to RGB. If colors still seem off, the original file may have embedded color profiles that require additional handling.

### Performance Tips

- For best performance, upload images in batches of 20-50 at a time
- Very large source files (>20MB) or RAW formats may take longer to process
- The app runs entirely in-memory, so available RAM may limit batch sizes
- Consider resizing extremely large images (>10000px) before upload for faster processing

### Format-Specific Notes

**RAW Formats**: Require additional system libraries. Processing is slower but produces high-quality results.

**PSD Files**: Supported for reading, but layers are flattened. Transparency is preserved.

**SVG/EPS**: Vector formats are rasterized at their default resolution before resizing.

**Animated GIFs**: Only the first frame is converted. Animation is not preserved.

**Multi-page PDFs**: Only the first page is converted to an image.

**DICOM**: Medical images are converted using standard windowing. May not preserve all medical metadata.

## Contributing

Contributions are welcome! Here are some ways you can help:

- Report bugs or request features by opening an issue
- Submit pull requests with improvements or bug fixes
- Add support for additional image formats
- Improve documentation or add examples
- Enhance error handling for edge cases
- Share the app with others who might find it useful

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly with various formats
4. Commit with clear messages: `git commit -m "Add feature description"`
5. Push to your fork: `git push origin feature-name`
6. Open a pull request

### Testing Checklist

When contributing, please test with:
- Common formats (JPG, PNG, GIF)
- Modern formats (HEIC, AVIF, WEBP)
- Images with transparency
- Large files (>10MB)
- Batch uploads (10+ files)
- Edge cases (1x1 pixel, grayscale, CMYK)

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions:
- Open an issue on GitHub with format details and error messages
- Check existing issues for similar problems
- Review the troubleshooting section above
- For format-specific issues, mention the exact format and source

## Acknowledgments

Built with [Streamlit](https://streamlit.io) and [Pillow](https://python-pillow.org), two excellent open-source projects that make Python web development and image processing accessible and enjoyable.

Special thanks to the maintainers of format-specific libraries that enable support for specialized formats like RAW, DICOM, and FITS.

---

**Made with ❤️ for universal image conversion - supporting 70+ formats!**
