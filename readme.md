# 🖼️ Image Format Converter

A powerful, user-friendly web application built with Streamlit that automatically converts images to optimal formats while intelligently handling transparency and resizing.

## Features

### Smart Format Detection
The app automatically analyzes each image and converts it to the most appropriate format:
- **PNG** for images with transparency (alpha channels)
- **JPG** for opaque images (smaller file sizes)

### Intelligent Resizing
All images are automatically resized to a maximum dimension of 1000 pixels (width or height) while maintaining their original aspect ratio. This ensures manageable file sizes without sacrificing quality.

### Batch Processing
Upload and convert multiple images simultaneously with a visual progress indicator showing real-time conversion status.

### Flexible Download Options
- Download all converted images in a single ZIP file
- Download individual images separately
- View detailed information about each converted image (format, dimensions)

### Supported Input Formats
- WEBP
- GIF
- PNG
- JPEG / JPG
- JFIF
- TIFF
- BMP
- SVG
- HEIF / HEIC
- AVIF
- EPS

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

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser and navigate to the local URL displayed in the terminal (typically `http://localhost:8501`)

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

6. Click "Deploy"

Your app will be live at `https://your-app-name.streamlit.app` within minutes!

### Deploy to Other Platforms

The app can also be deployed to:
- **Heroku**: Add a `Procfile` with `web: streamlit run app.py --server.port=$PORT`
- **Google Cloud Run**: Containerize with Docker and deploy
- **AWS EC2**: Run on a virtual machine with the installation steps above

## Usage

### Basic Workflow

1. **Upload Images**: Click the "Choose image files" button and select one or more images from your computer

2. **Automatic Processing**: The app will:
   - Analyze each image for transparency
   - Resize images to max 1000px dimension
   - Convert to PNG (if transparent) or JPG (if opaque)
   - Display conversion results

3. **Download Results**:
   - Click "Download All as ZIP" for a single archive
   - Or expand "Download Individual Files" for separate downloads

### Example Use Cases

**Photography Workflow**: Batch convert and resize camera photos to web-friendly JPG format at 1000px for portfolio websites or social media.

**Logo and Graphics**: Convert logos with transparency to optimized PNG files while maintaining quality and reducing file size.

**Mixed Media Projects**: Upload various format types and let the app intelligently choose the best output format based on each image's characteristics.

## Technical Details

### Image Processing Pipeline

The application follows this processing sequence for each uploaded image:

1. **Format Detection**: Opens the image and identifies its current format and color mode
2. **Transparency Check**: Analyzes alpha channels and palette transparency
3. **Mode Conversion**: Converts to RGBA (if transparent) or RGB (if opaque)
4. **Resizing**: Scales image to max 1000px using high-quality Lanczos resampling
5. **Output Selection**: Chooses PNG or JPG based on transparency
6. **Optimization**: Applies format-specific optimization (JPG quality: 95%, PNG: optimized)
7. **Packaging**: Collects all converted images for download

### Quality Settings

- **JPEG Quality**: 95% (excellent quality with reasonable compression)
- **PNG Optimization**: Enabled (reduces file size without quality loss)
- **Resampling Method**: Lanczos (highest quality resizing algorithm)

### Transparency Detection

The app checks for transparency through multiple methods:
- Direct alpha channel analysis in RGBA and LA modes
- Palette transparency detection in indexed color (P mode)
- Conversion testing for ambiguous formats

## Dependencies

```
streamlit - Web application framework
pillow - Image processing library
```

Full version specifications are available in `requirements.txt`.

## Troubleshooting

### Common Issues

**Issue**: "Module not found" error when running
**Solution**: Ensure all dependencies are installed with `pip install -r requirements.txt`

**Issue**: Some image formats not uploading
**Solution**: Verify the file extension matches one of the supported formats. Some exotic formats may require additional system libraries.

**Issue**: Large images causing slow processing
**Solution**: This is expected behavior for very large source images. The resizing step may take a few seconds per image.

**Issue**: SVG or EPS files not converting properly
**Solution**: These vector formats may require additional system dependencies (e.g., ghostscript for EPS). Install them separately based on your operating system.

### Performance Tips

- For best performance, upload images in batches of 20-50 at a time
- Very large source files (>20MB) may take longer to process
- The app runs entirely in-memory, so available RAM may limit batch sizes

## Contributing

Contributions are welcome! Here are some ways you can help:

- Report bugs or request features by opening an issue
- Submit pull requests with improvements or bug fixes
- Improve documentation or add examples
- Share the app with others who might find it useful

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit with clear messages: `git commit -m "Add feature description"`
5. Push to your fork: `git push origin feature-name`
6. Open a pull request

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check existing issues for similar problems
- Review the troubleshooting section above

## Acknowledgments

Built with [Streamlit](https://streamlit.io) and [Pillow](https://python-pillow.org), two excellent open-source projects that make Python web development and image processing accessible and enjoyable.

---

**Made with ❤️ for easy image conversion**
