# 🖼️ AI Image Captioning Web App

An intelligent web application that automatically generates captions for images using BLIP (Bootstrapped Language-Image Pre-training) AI model. Simply provide an image URL or website URL, and get AI-powered descriptions!

## ✨ Features

- **Direct Image Captioning**: Process single images from URLs
- **Website Image Extraction**: Automatically finds and captions all images on any website
- **Interactive Navigation**: Browse through multiple images with Previous/Next controls
- **Real-time Processing**: Live image processing with progress feedback
- **Web Interface**: Clean, user-friendly Gradio interface
- **Error Handling**: Robust error handling with informative messages

## 🚀 Demo

![Demo Screenshot](https://via.placeholder.com/800x400/4CAF50/white?text=AI+Image+Captioning+Demo)

### Example Outputs:
- **Input**: `https://example.com/cat.jpg`
- **Output**: "A orange tabby cat sitting on a wooden chair"

- **Input**: `https://news.com` (website)
- **Output**: Processes all images found on the site with individual captions

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-image-captioning.git
cd ai-image-captioning
```

2. **Create virtual environment**
```bash
python -m venv my_env
# Windows
my_env\Scripts\activate
# Linux/Mac
source my_env/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser** and go to `http://localhost:7860`

## 📦 Dependencies

- **gradio**: Web interface framework
- **transformers**: Hugging Face AI models
- **torch**: PyTorch deep learning framework
- **pillow**: Image processing
- **requests**: HTTP requests
- **beautifulsoup4**: Web scraping
- **numpy**: Numerical computing

## 🎯 Usage

### Single Image Captioning
1. Enter a direct image URL (e.g., `https://example.com/photo.jpg`)
2. Click "Generate Captions"
3. View the AI-generated caption

### Website Image Captioning
1. Enter a website URL (e.g., `https://news.com`)
2. Click "Generate Captions"
3. Use Previous/Next buttons to navigate through all found images
4. Each image displays with its individual caption

### Supported Image Formats
- JPG/JPEG
- PNG
- GIF
- BMP
- WebP
- TIFF

## 🧠 How It Works

1. **URL Detection**: Determines if input is direct image or website
2. **Web Scraping**: Extracts image URLs from websites using BeautifulSoup
3. **Image Processing**: Downloads and preprocesses images
4. **AI Inference**: Uses BLIP model to generate captions
5. **Display**: Shows results in interactive web interface

## 🔧 Technical Details

- **AI Model**: Salesforce BLIP (blip-image-captioning-base)
- **Framework**: Gradio for web interface
- **Image Processing**: PIL/Pillow for image handling
- **Web Scraping**: BeautifulSoup4 for HTML parsing
- **Backend**: PyTorch for AI computations

## 📁 Project Structure

```
ai-image-captioning/
├── app.py              # Main application
├── requirements.txt    # Dependencies
├── README.md          # Documentation
└── .gitignore         # Git ignore rules
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Salesforce** for the BLIP model
- **Hugging Face** for the transformers library
- **Gradio** for the web interface framework

## 🐛 Known Issues

- Large websites may take time to process all images
- Some websites may block automated requests
- Very large images may cause memory issues

## 🔮 Future Enhancements

- [ ] Batch image upload support
- [ ] Custom model selection
- [ ] Caption editing and saving
- [ ] Multi-language support
- [ ] Image filtering options
- [ ] Export functionality

---

**Made with ❤️ and AI**