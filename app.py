import os
import uuid
import time
import threading
import datetime
from flask import Flask, render_template, request, send_file, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
from wand.image import Image
from wand.exceptions import WandException

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Allowed and output formats
ALLOWED_EXTENSIONS = {
    'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'heic', 'heif', 'avif',
    'apng', 'jp2', 'j2k', 'cr2', 'nef', 'dng', 'psd', 'pdf', 'exr', 'svg',
    'eps', 'ai', 'indd', 'svgz', 'ico', 'tga', 'pict', 'xcf',
    'animated_webp', 'jpegxl', 'raw'
}

OUTPUT_FORMATS = {
    'jpg': 'JPEG', 'jpeg': 'JPEG', 'png': 'PNG', 'gif': 'GIF', 'bmp': 'Bitmap',
    'tiff': 'TIFF', 'webp': 'WebP', 'heic': 'HEIC', 'avif': 'AVIF',
    'apng': 'APNG', 'jp2': 'JPEG 2000', 'cr2': 'Canon RAW (CR2)',
    'nef': 'Nikon RAW (NEF)', 'dng': 'Adobe DNG', 'psd': 'Photoshop (PSD)',
    'pdf': 'PDF', 'svg': 'SVG', 'eps': 'EPS', 'ai': 'Adobe Illustrator (AI)',
    'ico': 'ICO', 'tga': 'TGA', 'pict': 'PICT', 'xcf': 'GIMP XCF',
    'exr': 'OpenEXR', 'svgz': 'Compressed SVG', 'jpegxl': 'JPEG XL'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Background thread for cleanup every 24 hrs
def cleanup_uploads_folder():
    while True:
        print(f"[CLEANUP] Running at {datetime.datetime.now()}")
        try:
            for filename in os.listdir(UPLOAD_FOLDER):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"[CLEANUP] Deleted {file_path}")
        except Exception as e:
            print(f"[CLEANUP ERROR] {str(e)}")
        time.sleep(86400)  # 24 hours

threading.Thread(target=cleanup_uploads_folder, daemon=True).start()

# Routes
@app.route('/')
def index():
    return render_template('index.html', formats=OUTPUT_FORMATS)

@app.route('/about')
def about():
    return render_template('about.html', formats=OUTPUT_FORMATS)

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/convert', methods=['POST'])
def convert_image():
    if 'file' not in request.files:
        flash('No file part in the request.')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'No file part in request.'}), 400
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('No file selected.')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'No file selected.'}), 400
        return redirect(url_for('index'))

    if not allowed_file(file.filename):
        flash('Unsupported file type.')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'Unsupported file type.'}), 400
        return redirect(url_for('index'))

    output_format = request.form.get('format', 'png').lower()
    if output_format not in OUTPUT_FORMATS:
        flash('Unsupported output format.')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'Unsupported output format.'}), 400
        return redirect(url_for('index'))

    input_path = None
    output_path = None

    try:
        filename = secure_filename(file.filename)
        uid = str(uuid.uuid4())
        input_path = os.path.join(UPLOAD_FOLDER, f"{uid}_{filename}")
        output_filename = f"{uid}_{os.path.splitext(filename)[0]}.{output_format}"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)

        file.save(input_path)

        with Image(filename=input_path) as img:
            # Resize if output is ICO and size too big
            if output_format == 'ico':
                MAX_ICO_SIZE = 256
                if img.width > MAX_ICO_SIZE or img.height > MAX_ICO_SIZE:
                    img.resize(MAX_ICO_SIZE, MAX_ICO_SIZE)
                    flash("Image was resized to 256x256 for ICO format.")

            # Set JPG quality
            if output_format in ['jpg', 'jpeg']:
                img.compression_quality = 90

            img.save(filename=output_path)

        return send_file(output_path, as_attachment=True, download_name=output_filename)

    except WandException as e:
        error_msg = f"Error converting image: {str(e)}"
        flash(error_msg)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': error_msg}), 400
        return redirect(url_for('index'))

    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        flash(error_msg)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': error_msg}), 500
        return redirect(url_for('index'))

    finally:
        try:
            if input_path and os.path.exists(input_path):
                os.remove(input_path)
        except Exception as e:
            print(f"Error deleting input: {str(e)}")
        try:
            if output_path and os.path.exists(output_path):
                os.remove(output_path)
        except Exception as e:
            print(f"Error deleting output: {str(e)}")

# Error handlers
@app.errorhandler(413)
def too_large(e):
    msg = 'The file is too large. Max allowed size is 16MB.'
    flash(msg)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'error': msg}), 413
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    msg = "Internal server error. Please try again later."
    flash(msg)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'error': msg}), 500
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)

