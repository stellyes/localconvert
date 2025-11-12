# LocalConvert - Custom Image Processor

A powerful, versatile web application built with Streamlit that offers format conversion from 70+ formats and AI-powered image upscaling using Cloudinary's Generative AI. The app intelligently handles transparency, resizing, and uses cloud-based AI processing for high-quality upscaling without local GPU requirements.

## Features

### Dual Processing Modes

**Format Conversion Mode:**
- Convert from 70+ image formats to optimal web formats
- Automatic PNG/JPG selection based on transparency
- Intelligent resizing to 1000px maximum dimension
- Batch processing with progress tracking

**AI Upscaling Mode:**
- 2x, 3x, or 4x upscaling using Cloudinary's Generative AI
- Cloud-based processing - no local GPU needed
- Automatic face detection and enhancement
- Super-resolution quality enhancement
- Works on any device with internet connection
- No installation of heavy ML libraries required

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

### Cloudinary AI Integration
Uses Cloudinary's advanced AI upscaling technology:
- No API rate limits (based on your Cloudinary plan)
- Cloud-based processing works on any device
- Automatic face detection and enhancement
- Super-resolution quality
- No local GPU required
- Multiple scale factors (2x, 3x, 4x)
- Free tier available for personal use

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

### Cloudinary Credentials Setup

For AI upscaling functionality, you need a Cloudinary account:

1. Sign up at [Cloudinary.com](https://cloudinary.com/) (free tier available)
2. Get your credentials from the dashboard:
   - Cloud Name
   - API Key
   - API Secret

3. Add to `.streamlit/secrets.toml`:
```toml
app_password = "password"
cloudinary_cloud_name = "your-cloud-name"
cloudinary_api_key = "your-api-key"
cloudinary_api_secret = "your-api-secret"
```

4. For Streamlit Cloud, add to app secrets:
```toml
app_password = "password"
cloudinary_cloud_name = "your-cloud-name"
cloudinary_api_key = "your-api-key"
cloudinary_api_secret = "your-api-secret"
```

**Cloudinary Free Tier:**
- 25 monthly credits (transformations)
- 25GB storage
- 25GB monthly bandwidth
- Perfect for personal use and testing

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Cloudinary account (for AI upscaling)

### Local Installation

1. Clone this repository or download the files:
```bash
git clone <your-repository-url>
cd image-processor
```

2. Create a `.streamlit` directory and `secrets.toml` file:
```bash
mkdir .streamlit
```

3. Create `.streamlit/secrets.toml` with your credentials:
```toml
app_password = "password"
cloudinary_cloud_name = "your-cloud-name"
cloudinary_api_key = "your-api-key"
cloudinary_api_secret = "your-api-secret"
```

4. Add secrets to `.gitignore`:
```bash
echo '.streamlit/secrets.toml' >> .gitignore
```

5. Install required dependencies:
```bash
pip install -r requirements.txt
```

6. Run the application:
```bash
streamlit run app.py
```

7. Enter the password when prompted (default: "password")

8. Open your browser and navigate to the local URL displayed in the terminal (typically `http://localhost:8501`)

## Deployment

### Deploy to Streamlit Cloud

1. Push your code to a GitHub repository with the following structure:
```
your-repo/
├── app.py
├── requirements.txt
└── README.md
```

**Important**: Do NOT include `.streamlit/secrets.toml` in your repository!

2. Visit [share.streamlit.io](https://share.streamlit.io)

3. Sign in with your GitHub account

4. Click "New app"

5. Select your repository, branch, and main file (`app.py`)

6. **Important**: Before deploying, add secrets:
   - In your app dashboard, go to "Settings" → "Secrets"
   - Add the following:
   ```toml
   app_password = "your-secure-password"
   cloudinary_cloud_name = "your-cloud-name"
   cloudinary_api_key = "your-api-key"
   cloudinary_api_secret = "your-api-secret"
   ```

7. Click "Deploy"

Your app will be live at `https://your-app-name.streamlit.app` within minutes!

**On Streamlit Cloud:**
- ✅ Format conversion works perfectly
- ✅ AI upscaling works via Cloudinary (cloud-based)
- ✅ No GPU required
- ✅ Fast processing

### Deploy to Other Platforms

The app can also be deployed to:
- **Heroku**: Add environment variables for secrets
- **Google Cloud Run**: Use Secret Manager for credentials
- **AWS Elastic Beanstalk**: Configure environment variables
- **Any platform with Python support**: Set environment variables or use secrets management

## Usage

### Basic Workflow

1. **Login**: Enter the password when prompted

2. **Upload Images**: Click the "Choose image files" button and select one or more images from your computer (supports 70+ formats!)

3. **Choose Operation**:
   - **Convert & Resize**: Optimize format and resize to 1000px max
   - **AI Upscale (Cloudinary)**: Enhance quality using AI (2x, 3x, or 4x)

4. **Select Upscale Factor** (if using AI Upscale):
   - 2x: Doubles the resolution (recommended for most uses)
   - 3x: Triples the resolution
   - 4x: Quadruples the resolution (best quality, larger files)

5. **Process**: Click "🚀 Process Images" to start

6. **Automatic Processing**: The app will:
   - Show real-time progress
   - Upload to Cloudinary (if upscaling)
   - Apply AI transformations
   - Download processed images
   - Display detailed results for each file

7. **Review Results**: See a detailed breakdown showing:
   - Filename
   - Processing method (conversion or upscale type)
   - Final dimensions in pixels
   - File size in kilobytes

8. **Download Results**:
   - Click "Download All as ZIP" for a single archive
   - Or expand "Download Individual Files" for separate downloads

### Example Use Cases

**Photography Workflow**: Convert RAW camera files to web-friendly JPG format, then upscale select images for print or large displays.

**Web Optimization**: Batch convert and resize images to optimal web formats, reducing page load times while maintaining quality.

**Image Enhancement**: Upscale low-resolution photos for better quality in presentations, prints, or high-DPI displays.

**Old Photo Restoration**: Convert scanned photos from legacy formats, then upscale with AI to recover detail and improve clarity.

**Professional Design**: Convert Photoshop PSD files to web formats, with AI upscaling for final high-res outputs.

**E-commerce**: Upscale product images for better detail and quality, with automatic face enhancement for portraits.

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

1. **Image Upload**: Securely uploads image to Cloudinary
2. **AI Processing**: Cloudinary applies generative AI upscaling:
   - Face detection and enhancement (if faces present)
   - Super-resolution algorithms
   - Detail preservation and enhancement
3. **URL Generation**: Creates optimized delivery URL with transformations
4. **Download**: Retrieves the upscaled image
5. **Cleanup**: Automatically removes temporary files from Cloudinary
6. **Packaging**: Prepares upscaled images for download

### Cloudinary's AI Technology

Cloudinary's upscaling uses advanced generative AI:

**Key Features:**
- **Face Detection**: Automatically detects and enhances faces with specialized algorithms
- **Super-Resolution**: Uses AI trained on millions of images to intelligently add detail
- **Generative AI**: Creates realistic details rather than simple interpolation
- **Content-Aware**: Understands image content to preserve important features
- **Quality Optimization**: Automatically selects best format and compression

**How It Works:**
- Analyzes image content and structure
- Applies specialized algorithms for different image types
- Uses machine learning models trained on diverse datasets
- Generates new pixels based on learned patterns
- Preserves edges, textures, and fine details

**Performance:**
- Cloud-based: No local resources required
- Fast processing: Typically 2-10 seconds per image
- Scalable: Handles images up to 100 megapixels
- Reliable: 99.9% uptime SLA

**Face Enhancement:**
When faces are detected, Cloudinary applies additional generative AI specifically trained on faces to ensure:
- Natural appearance
- Clear facial features
- Proper skin texture
- No artificial smoothing
- Enhanced clarity

### Quality Settings

- **JPEG Quality**: 95% (excellent quality with reasonable compression)
- **PNG Optimization**: Enabled (reduces file size without quality loss)
- **Resampling Method**: Lanczos (highest quality resizing algorithm)
- **Cloudinary Quality**: auto:best (automatic optimal quality selection)
- **AI Model**: Cloudinary Generative Upscale with face detection

## Dependencies

### Core Dependencies
```
streamlit>=1.28.0 - Web application framework
pillow>=10.0.0 - Image processing library
cloudinary>=1.36.0 - Cloudinary Python SDK
requests>=2.31.0 - HTTP library for downloads
```

**Note**: No heavy ML libraries required! All AI processing is done in the cloud via Cloudinary's API.

Full version specifications are available in `requirements.txt`.

## Troubleshooting

### Common Issues

**Issue**: "Cloudinary not configured" message
**Solution**: Add your Cloudinary credentials to Streamlit secrets as shown in the setup section. Get free credentials at https://cloudinary.com/

**Issue**: Upscaling fails with authentication error
**Solution**: Verify your Cloudinary credentials are correct. Check your API key and secret in the Cloudinary dashboard.

**Issue**: Images not appearing after upscaling
**Solution**: Check your Cloudinary plan limits. Free tier has 25 monthly credits. Upgrade if needed or wait for monthly reset.

**Issue**: Slow upscaling
**Solution**: This is normal for cloud processing. Large images or 4x upscaling takes longer. Typically 2-10 seconds per image depending on size.

**Issue**: Password protection not working after deployment
**Solution**: Ensure you've added `app_password` to your Streamlit Cloud secrets (not just local secrets.toml).

**Issue**: "Module not found" error when running
**Solution**: Ensure all dependencies are installed with `pip install -r requirements.txt`

**Issue**: Cloudinary quota exceeded
**Solution**: You've reached your monthly transformation limit. Either:
- Wait for monthly reset
- Upgrade your Cloudinary plan
- Use basic Lanczos upscaling (app will fall back automatically)

### Cloudinary-Specific Issues

**Issue**: Upload fails with "Invalid signature"
**Solution**: Check that your API secret is correct and there are no extra spaces in your secrets.toml.

**Issue**: Upscaled images look different from originals
**Solution**: This is expected - AI upscaling enhances details and may improve colors/contrast. Use lower scale factors (2x instead of 4x) for more subtle changes.

**Issue**: Large images timing out
**Solution**: Very large images (>20MB) may take longer. Consider:
- Using 2x instead of 4x upscaling
- Processing fewer images at once
- Resizing images before upscaling

### Performance Tips

- For format conversion, batch process 20-50 images at a time
- For AI upscaling, process 5-10 images at a time for optimal performance
- Use 2x upscaling for faster processing and smaller output files
- 4x upscaling produces best quality but larger files and longer processing time
- Monitor your Cloudinary usage in their dashboard
- Free tier is suitable for 20-25 images per month (depending on settings)

## Cloudinary Pricing & Limits

**Free Tier:**
- 25 monthly transformation credits
- 25GB storage
- 25GB monthly bandwidth
- Perfect for personal use
- No credit card required

**Paid Plans:**
- Start at $89/month
- More transformations and bandwidth
- Advanced features
- Priority support
- Custom configurations

**Transformation Costs:**
- Basic transformations: 1 credit each
- Generative AI (including upscale): Higher credit cost
- Monitor usage in Cloudinary dashboard
- Set usage alerts to avoid overages

**Best Practices:**
- Use 2x upscaling to conserve credits
- Process only images that truly need upscaling
- Convert images first, then upscale selectively
- Monitor your monthly usage

## Comparison: Cloudinary vs Other Solutions

**Cloudinary (This App):**
- ✅ Cloud-based, works anywhere
- ✅ No GPU required
- ✅ State-of-the-art generative AI
- ✅ Automatic face enhancement
- ✅ Fast processing (2-10 seconds)
- ✅ Works on Streamlit Cloud
- ✅ Free tier available
- ✅ Easy setup
- ❌ Requires API key
- ❌ Monthly limits on free tier
- ❌ Requires internet connection

**Local ML Solutions (Real-ESRGAN, etc.):**
- ✅ Unlimited processing
- ✅ Works offline
- ✅ Free forever
- ❌ Requires GPU for good performance
- ❌ Complex installation
- ❌ Large model downloads
- ❌ Won't work on Streamlit Cloud
- ❌ Slow on CPU (30-60s per image)

## Contributing

Contributions are welcome! Here are some ways you can help:

- Report bugs or request features by opening an issue
- Submit pull requests with improvements or bug fixes
- Add support for additional image processors
- Improve error handling and user feedback
- Enhance documentation or add examples
- Share the app with others who might find it useful

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly with various formats
4. Test both processing modes (convert and upscale)
5. Test with and without Cloudinary credentials
6. Commit with clear messages: `git commit -m "Add feature description"`
7. Push to your fork: `git push origin feature-name`
8. Open a pull request

### Testing Checklist

When contributing, please test:
- Password protection (correct/incorrect passwords)
- Both processing modes (convert and upscale)
- Different upscale factors (2x, 3x, 4x)
- Common formats (JPG, PNG, GIF)
- Images with transparency
- Large files (>10MB)
- Batch uploads (10+ files)
- Error handling (missing credentials, network issues)
- Fallback to Lanczos when Cloudinary not configured

## License

This project is open source and available under the MIT License.

Cloudinary is a commercial service with a free tier. See their website for terms of service.

## Support

If you encounter any issues or have questions:
- Open an issue on GitHub with detailed error messages
- Check existing issues for similar problems
- Review the troubleshooting section above
- For Cloudinary-specific issues, consult [Cloudinary documentation](https://cloudinary.com/documentation)
- Check your Cloudinary usage and limits in their dashboard

## Acknowledgments

Built with [Streamlit](https://streamlit.io) and [Pillow](https://python-pillow.org), two excellent open-source projects that make Python web development and image processing accessible.

AI upscaling powered by [Cloudinary](https://cloudinary.com/), providing state-of-the-art generative AI for image enhancement that's accessible, reliable, and easy to integrate.

Special thanks to:
- The Cloudinary team for their powerful media API
- The Streamlit team for the amazing web framework
- All contributors to the image processing ecosystem

---

**Made with ❤️ for universal image processing - Convert & Upscale with Cloud AI Power!**

