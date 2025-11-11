# 🖼️ AI Image Processor

A powerful, versatile web application built with Streamlit that offers two key features: format conversion from 70+ formats and AI-powered image upscaling using Real-ESRGAN. The app intelligently handles transparency, resizing, and uses local AI processing for high-quality upscaling without API limits.

## Features

### Dual Processing Modes

**Format Conversion Mode:**
- Convert from 70+ image formats to optimal web formats
- Automatic PNG/JPG selection based on transparency
- Intelligent resizing to 1000px maximum dimension
- Batch processing with progress tracking

**AI Upscaling Mode:**
- 2x or 4x upscaling using Real-ESRGAN
- Local processing - no API calls or rate limits
- Enhances image quality and adds detail
- GPU acceleration support (CUDA)
- Completely free and open source
- Works offline

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

### Real-ESRGAN Integration
Uses the state-of-the-art Real-ESRGAN model for AI upscaling:
- No API keys required
- No rate limits or usage costs
- Local processing for privacy
- GPU acceleration when available
- CPU fallback mode included
- Multiple scale factors (2x, 4x)

### Comprehensive File Information
View detailed information about each conversion:
- Original format → Output format (or upscale factor)
- Final dimensions
- File size in KB

### Flexible Download Options
- Download all processed images in a single ZIP file
- Download individual images separately
- Full-width download button for easy access

### Password Protection
Built-in password authentication to restrict access to authorized users only.

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
- Python 3.8 or higher
- pip (Python package installer)
- (Optional) CUDA-compatible GPU for faster AI upscaling

### Local Installation

1. Clone this repository or download the files:
```bash
git clone <your-repository-url>
cd image-processor
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

5. Install Real-ESRGAN for AI upscaling (optional but recommended):

**For GPU users (NVIDIA with CUDA):**
```bash
# Install PyTorch with CUDA support first
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Install Real-ESRGAN and dependencies
pip install basicsr
pip install facexlib
pip install gfpgan
pip install realesrgan
```

**For CPU-only users:**
```bash
# Install PyTorch (CPU version)
pip install torch torchvision

# Install Real-ESRGAN and dependencies
pip install basicsr
pip install facexlib
pip install gfpgan
pip install realesrgan
```

**Note**: CPU processing is significantly slower than GPU. A single 4x upscale might take 30-60 seconds on CPU vs 2-5 seconds on GPU.

6. For RAW format support, install additional system libraries:

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

7. Run the application:
```bash
streamlit run app.py
```

8. Enter the password when prompted (default: "password")

9. Open your browser and navigate to the local URL displayed in the terminal (typically `http://localhost:8501`)

## Deployment

### Deploy to Streamlit Cloud

**Important**: Streamlit Cloud does not support GPU acceleration, so AI upscaling will run in CPU mode and be significantly slower. For production use with upscaling, consider deploying to a platform with GPU support.

1. Push your code to a GitHub repository with the following structure:
```
your-repo/
├── app.py
├── requirements.txt
└── README.md
```

**Important**: Do NOT include `.streamlit/secrets.toml` in your repository!

2. Create a `requirements.txt` file with the following:
```
streamlit
pillow
torch
torchvision
basicsr
facexlib
gfpgan
realesrgan
```

3. Visit [share.streamlit.io](https://share.streamlit.io)

4. Sign in with your GitHub account

5. Click "New app"

6. Select your repository, branch, and main file (`app.py`)

7. **Important**: Before deploying, add secrets:
   - In your app dashboard, go to "Settings" → "Secrets"
   - Add the following:
   ```toml
   app_password = "your-secure-password"
   ```

8. Click "Deploy"

Your app will be live at `https://your-app-name.streamlit.app` within minutes!

**Performance Note**: AI upscaling on Streamlit Cloud will be slow due to CPU-only processing. Consider alternative deployment options for better performance.

### Deploy with GPU Support

For optimal AI upscaling performance, deploy to a platform with GPU support:

**Google Cloud Run with GPU:**
1. Create a Docker container with CUDA support
2. Include PyTorch with CUDA
3. Deploy to Cloud Run with GPU-enabled instances
4. Set appropriate memory and CPU limits

**AWS EC2 with GPU:**
1. Launch a GPU instance (e.g., g4dn.xlarge)
2. Install CUDA and cuDNN
3. Follow local installation steps
4. Use systemd or supervisor to run Streamlit as a service
5. Set up nginx as a reverse proxy

**Vast.ai / RunPod:**
1. Rent a GPU instance
2. Use a pre-configured PyTorch container
3. Install Streamlit and dependencies
4. Run the app with port forwarding

### System Requirements for GPU

- **NVIDIA GPU**: GTX 1060 or better (6GB+ VRAM recommended)
- **CUDA**: Version 11.7 or 11.8
- **Driver**: Latest NVIDIA drivers
- **RAM**: 8GB+ system RAM
- **Storage**: 2GB+ for models

## Usage

### Basic Workflow

1. **Login**: Enter the password when prompted

2. **Upload Images**: Click the "Choose image files" button and select one or more images from your computer (supports 70+ formats!)

3. **Choose Operation**:
   - **Convert & Resize**: Optimize format and resize to 1000px max
   - **AI Upscale**: Enhance quality using Real-ESRGAN (2x or 4x)

4. **Select Upscale Factor** (if using AI Upscale):
   - 2x: Doubles the resolution
   - 4x: Quadruples the resolution (larger files)

5. **Process**: Click "🚀 Process Images" to start

6. **Automatic Processing**: The app will:
   - Show real-time progress
   - Process each image according to your selected operation
   - Display detailed results for each file

7. **Review Results**: See a detailed breakdown showing:
   - Filename
   - Original format → Output format (or upscale factor)
   - Final dimensions in pixels
   - File size in kilobytes

8. **Download Results**:
   - Click "Download All as ZIP" for a single archive
   - Or expand "Download Individual Files" for separate downloads

### Example Use Cases

**Photography Workflow**: Convert RAW camera files to web-friendly JPG format, then upscale select images 4x for print or large displays.

**Web Optimization**: Batch convert and resize images to optimal web formats, reducing page load times while maintaining quality.

**Image Enhancement**: Upscale low-resolution photos 2x or 4x for better quality in presentations, prints, or high-DPI displays.

**Old Photo Restoration**: Convert scanned photos from legacy formats, then upscale 4x to recover detail and improve clarity.

**Professional Design**: Convert Photoshop PSD files to web formats, with AI upscaling for final high-res outputs.

**Game Asset Creation**: Upscale low-res textures or sprites for HD remasters.

**Social Media**: Resize images to optimal dimensions, then upscale for platforms requiring higher resolutions.

## Technical Details

### Format Conversion Pipeline

1. **Format Detection**: Opens the image and identifies its current format and color mode
2. **Mode Analysis**: Determines if special handling is needed (CMYK, palette, grayscale, etc.)
3. **Transparency Check**: Analyzes alpha channels and palette transparency
4. **Intelligent Conversion**: Converts to RGBA (if transparent) or RGB (if opaque)
5. **Resizing**: Scales image to max 1000px using Lanczos resampling
6. **Output Selection**: Chooses PNG or JPG based on transparency
7. **Optimization**: Applies format-specific optimization
8. **Packaging**: Collects all converted images for download

### AI Upscaling Pipeline

1. **Image Loading**: Opens and validates the input image
2. **Color Conversion**: Converts to RGB if necessary
3. **Array Conversion**: Converts PIL image to NumPy array
4. **AI Enhancement**: Real-ESRGAN model processes the image
5. **Reconstruction**: Converts enhanced array back to PIL Image
6. **Output**: Saves as optimized PNG
7. **Packaging**: Prepares upscaled images for download

### Real-ESRGAN Technology

Real-ESRGAN is a state-of-the-art image super-resolution model that uses Generative Adversarial Networks (GANs) to enhance image quality:

**Key Features:**
- Trained on real-world degraded images
- Handles complex degradation patterns
- Preserves fine details and textures
- Reduces artifacts and noise
- Works on various image types (photos, art, screenshots)

**Model Architecture:**
- Based on RRDB (Residual in Residual Dense Block)
- 23 residual blocks
- 64 feature channels
- Trained with perceptual and adversarial losses

**Performance:**
- GPU (CUDA): 2-5 seconds per image (4x upscale, 1080p input)
- CPU: 30-60 seconds per image (4x upscale, 1080p input)
- Memory: ~2GB VRAM for 4K images

**Limitations:**
- Cannot fix heavily blurred or out-of-focus images
- Best results with sharp, detailed input images
- Very large images (>4K) may require tiling
- Requires good quality input for optimal results

### Quality Settings

- **JPEG Quality**: 95% (excellent quality with reasonable compression)
- **PNG Optimization**: Enabled (reduces file size without quality loss)
- **Resampling Method**: Lanczos (highest quality resizing algorithm)
- **AI Model**: RealESRGAN_x4plus (trained on diverse dataset)
- **Precision**: FP16 (half precision) on GPU, FP32 on CPU

## Dependencies

### Core Dependencies
```
streamlit>=1.28.0 - Web application framework
pillow>=10.0.0 - Image processing library
```

### AI Upscaling Dependencies
```
torch>=2.0.0 - Deep learning framework
torchvision>=0.15.0 - Computer vision utilities
basicsr>=1.4.2 - Basic image restoration toolkit
facexlib>=0.3.0 - Face detection and enhancement
gfpgan>=1.3.8 - Face restoration model
realesrgan>=0.3.0 - Real-ESRGAN implementation
numpy>=1.24.0 - Numerical computing
opencv-python>=4.8.0 - Computer vision library
```

### Optional Dependencies
```
rawpy - RAW camera format support
pydicom - DICOM medical imaging support
astropy - FITS astronomy format support
OpenEXR - HDR/EXR format support
```

Full version specifications are available in `requirements.txt`.

## Troubleshooting

### Common Issues

**Issue**: "AI Upscaling unavailable" message
**Solution**: Install Real-ESRGAN dependencies:
```bash
pip install torch torchvision basicsr facexlib gfpgan realesrgan
```

**Issue**: CUDA out of memory errors during upscaling
**Solution**: 
- Try upscaling smaller images
- Use 2x instead of 4x upscaling
- Close other GPU-intensive applications
- Enable tiling in the code (for very large images)

**Issue**: Very slow upscaling performance
**Solution**: 
- Verify GPU is being used (check app status message)
- Install CUDA-enabled PyTorch version
- Check NVIDIA drivers are up to date
- Consider using 2x upscaling instead of 4x

**Issue**: "ImportError: No module named 'basicsr'"
**Solution**: Install BasicSR and related packages:
```bash
pip install basicsr facexlib gfpgan
```

**Issue**: Password protection not working after deployment
**Solution**: Ensure you've added `app_password` to your Streamlit Cloud secrets (not just local secrets.toml).

**Issue**: "Module not found" error when running
**Solution**: Ensure all dependencies are installed with `pip install -r requirements.txt`

**Issue**: Model download fails
**Solution**: Check internet connection. Models are downloaded automatically on first use (~65MB for RealESRGAN_x4plus).

**Issue**: Images look worse after upscaling
**Solution**: AI upscaling works best on sharp, detailed images. Blurry or out-of-focus images won't improve significantly. Consider using the original or trying 2x instead of 4x.

### GPU-Specific Issues

**Issue**: "RuntimeError: CUDA error: out of memory"
**Solution**: 
```python
# Reduce batch size or use tiling (modify code)
upsampler = RealESRGANer(
    scale=4,
    model_path='...',
    model=model,
    tile=400,  # Enable tiling for large images
    tile_pad=10,
    pre_pad=0
)
```

**Issue**: GPU not detected (shows CPU mode)
**Solution**:
1. Check CUDA installation: `nvidia-smi`
2. Verify PyTorch CUDA: `python -c "import torch; print(torch.cuda.is_available())"`
3. Reinstall PyTorch with CUDA: `pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118`

### Performance Tips

- For format conversion, batch process 20-50 images at a time
- For AI upscaling (GPU), process 5-10 images at a time
- For AI upscaling (CPU), process 1-3 images at a time
- Very large source files (>10MB) may take longer to upload and process
- The app runs in-memory, so available RAM may limit batch sizes
- For best upscaling results, start with images that are at least 200x200px
- Use 2x upscaling for faster processing and smaller output files
- 4x upscaling produces larger files but maximum detail

## Comparison: Real-ESRGAN vs API Services

**Real-ESRGAN (This App):**
- ✅ Completely free, no rate limits
- ✅ Local processing, full privacy
- ✅ Works offline
- ✅ Open source
- ✅ GPU acceleration
- ✅ High quality results
- ❌ Requires setup/installation
- ❌ Needs GPU for good performance
- ❌ Takes up local resources

**API Services (DeepAI, etc.):**
- ✅ No installation required
- ✅ Works on any device
- ✅ Fast without GPU
- ❌ Requires API key
- ❌ Rate limits
- ❌ Costs money (usually)
- ❌ Requires internet
- ❌ Privacy concerns

## Contributing

Contributions are welcome! Here are some ways you can help:

- Report bugs or request features by opening an issue
- Submit pull requests with improvements or bug fixes
- Add support for additional upscaling models
- Improve error handling and user feedback
- Optimize performance for CPU/GPU
- Enhance documentation or add examples
- Share the app with others who might find it useful

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly with various formats
4. Test both processing modes (convert and upscale)
5. Test on both CPU and GPU if possible
6. Commit with clear messages: `git commit -m "Add feature description"`
7. Push to your fork: `git push origin feature-name`
8. Open a pull request

### Testing Checklist

When contributing, please test:
- Password protection (correct/incorrect passwords)
- Both processing modes (convert and upscale)
- Different upscale factors (2x, 4x)
- Common formats (JPG, PNG, GIF)
- Images with transparency
- Large files (>10MB)
- Batch uploads (10+ files)
- Error handling (missing dependencies, invalid images)
- Both GPU and CPU modes (if possible)

## License

This project is open source and available under the MIT License.

Real-ESRGAN is licensed under the BSD 3-Clause License.

## Support

If you encounter any issues or have questions:
- Open an issue on GitHub with detailed error messages
- Check existing issues for similar problems
- Review the troubleshooting section above
- For GPU/CUDA issues, check PyTorch documentation
- For model-specific issues, consult Real-ESRGAN repository

## Acknowledgments

Built with [Streamlit](https://streamlit.io) and [Pillow](https://python-pillow.org), two excellent open-source projects that make Python web development and image processing accessible.

AI upscaling powered by [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) by Xintao Wang and team, providing state-of-the-art image super-resolution technology that's free and open source.

Special thanks to:
- The Real-ESRGAN team for their groundbreaking research
- The BasicSR framework developers
- PyTorch team for the deep learning framework
- All contributors to the image processing ecosystem

## Citation

If you use Real-ESRGAN in your research, please cite:

```bibtex
@InProceedings{wang2021realesrgan,
    author    = {Xintao Wang and Liangbin Xie and Chao Dong and Ying Shan},
    title     = {Real-ESRGAN: Training Real-World Blind Super-Resolution with Pure Synthetic Data},
    booktitle = {International Conference on Computer Vision Workshops (ICCVW)},
    date      = {2021}
}
```

---

**Made with ❤️ for universal image processing - Convert & Upscale with Local AI Power!**
