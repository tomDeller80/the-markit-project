from matplotlib import font_manager
from PIL import Image, ImageTk
from pathlib import Path
import sys
import os

_FONT_CACHE = []

def hex_to_rgba(hex_color, opacity=255):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return rgb + (opacity,)

def scale_dimensions(width, height, scale_percent):
    ratio = float(scale_percent) / 100
    return int(width * ratio), int(height * ratio)

def get_center_pos(canvas_w, canvas_h, image_w, image_h):
    x = max(canvas_w, image_w) / 2
    y = max(canvas_h, image_h) / 2
    return x, y

def get_filename(path):
    return os.path.splitext(os.path.basename(path))[0]

def to_bool(value):
    return str(value).lower() in ("yes", "true", "t", "1")

def get_resource_path(relative_path):
    try:
        base_path = Path(sys._MEIPASS)
    except AttributeError:

        base_path = Path(__file__).resolve().parent

        if not (base_path / "static").exists():
            if (base_path.parent / "static").exists():
                base_path = base_path.parent

    full_path = base_path / relative_path
    return str(full_path)

def get_ttf_font_names():

    global _FONT_CACHE

    if _FONT_CACHE:
        return _FONT_CACHE

    ttf_paths = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')

    font_names = set()
    for path in ttf_paths:
        try:
            prop = font_manager.FontProperties(fname=path)
            name = prop.get_name()
            font_names.add(name)
        except Exception:
            continue

    _FONT_CACHE = sorted(list(font_names))
    return _FONT_CACHE

def load_icon(path, size=(20, 20)):
    try:
        resolved_path = get_resource_path(path)
        img = Image.open(resolved_path).resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading icon {path}: {e}")
        return None

def is_valid_image(file_path):
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')
    if os.path.isdir(file_path):
        return False, "You dropped a folder. Please drop a single image file."
    if not file_path.lower().endswith(valid_extensions):
        return False, f"Unsupported file type. Please use {', '.join(valid_extensions).upper()}."
    return True, None