import os
import uuid
from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_WIDTH = 1200
JPEG_QUALITY = 85


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(file, subfolder=''):
    """Save uploaded image, resize if > MAX_WIDTH, return filename."""
    if not file or not allowed_file(file.filename):
        return None

    ext = file.filename.rsplit('.', 1)[1].lower()
    if ext == 'jpg':
        ext = 'jpeg'

    unique_name = f'{uuid.uuid4().hex}.{ext}'
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, unique_name)

    img = Image.open(file.stream)

    # Convert RGBA to RGB for JPEG
    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGB')

    # Resize if too wide
    if img.width > MAX_WIDTH:
        ratio = MAX_WIDTH / img.width
        new_height = int(img.height * ratio)
        img = img.resize((MAX_WIDTH, new_height), Image.LANCZOS)

    save_ext = 'JPEG' if ext == 'jpeg' else ext.upper()
    if save_ext == 'JPEG':
        img.save(filepath, save_ext, quality=JPEG_QUALITY, optimize=True)
    else:
        img.save(filepath, save_ext)

    # Return relative path from uploads folder
    return os.path.join(subfolder, unique_name) if subfolder else unique_name


def delete_image(filename):
    """Delete an image file from uploads folder."""
    if not filename:
        return
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
