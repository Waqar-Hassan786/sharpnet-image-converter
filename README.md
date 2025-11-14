# SharpNet Image Converter

![SharpNet Logo](https://sharpnet-image-converter.onrender.com/static/logo.png)

**A free, fast, and privacy-focused online tool to convert between hundreds of image formats without any sign-ups.**

SharpNet is a lightweight web application designed for quick and easy image conversions. Built with Python and the powerful ImageMagick library, it provides a seamless user experience with a clean interface and robust functionality.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Key Features

*   **Extensive Format Support**: Convert between 200+ formats, including common types like **JPG, PNG, GIF, WebP**, professional formats like **PSD, AI, SVG**, and RAW photo formats like **CR2, NEF, ARW**.
*   **High-Quality Conversion**: Leverages the ImageMagick Wand library to maintain the best possible quality for your converted images.
*   **100% Free & Anonymous**: No registration, no accounts, and no watermarks. Convert your files instantly.
*   **Privacy First**: Your privacy is paramount. All uploaded and converted files are automatically deleted from our servers after conversion (or within 24 hours).
*   **User-Friendly Interface**: A clean, modern UI with drag-and-drop support for a smooth and intuitive workflow.
*   **Fast & Efficient**: Optimized for speed, so you can get your converted files in seconds.

## 🚀 Live Demo

You can try the live application here: **[sharpnet-image-converter.onrender.com](https://sharpnet-image-converter.onrender.com/)**


*(Suggestion: Replace this with a screenshot or GIF of your application's interface!)*

---

## 🛠️ Tech Stack

*   **Backend**: Python (Flask)
*   **Image Processing**: ImageMagick's Wand Library
*   **Frontend**: HTML, CSS, JavaScript (with Jinja2 for templating)
*   **Containerization**: Docker
*   **Deployment**: Render

---

## 🔧 Running the Project Locally

To run SharpNet on your local machine, you'll need **Python**, **pip**, and **ImageMagick** installed.

### 1. Prerequisites

*   **Install ImageMagick**: This is a crucial dependency. Follow the instructions for your operating system from the [official ImageMagick website](https://imagemagick.org/script/download.php).

### 2. Clone the Repository

```bash
git clone https://github.com/Waqar-Hassan786/sharpnet-image-converter.git
cd sharpnet-image-converter
```

### 3. Set Up a Virtual Environment & Install Dependencies

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install the required Python packages
pip install -r requirements.txt
```

### 4. Run the Application

```bash
# Run the Flask development server
flask run
```

The application will be available at `http://127.0.0.1:5000`.

### 5. Running with Docker

Alternatively, you can build and run the project using Docker.

```bash
# Build the Docker image
docker build -t sharpnet-converter .

# Run the Docker container
docker run -p 5000:5000 sharpnet-converter
```

---

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or want to fix a bug, please feel free to open an issue or submit a pull request.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/YourFeature`).
6.  Open a pull request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

*   **ImageMagick** for the powerful image processing capabilities.
*   **Flask** for the flexible and lightweight web framework.
*   **Render** for the easy-to-use deployment platform.
