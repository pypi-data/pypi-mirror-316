from PIL import Image
import numpy as np

def load_image(image_path: str) -> Image.Image:
    """Loads an image from the specified path."""
    return Image.open(image_path)

def resize_image(image: Image.Image, size: tuple) -> Image.Image:
    """Resizes the image to the specified size."""
    return image.resize(size)

def normalize_image(image: Image.Image) -> np.ndarray:
    """Normalizes the image to [0, 1]."""
    return np.asarray(image) / 255.0

def convert_to_grayscale(image: Image.Image) -> Image.Image:
    """Converts the image to grayscale."""
    return image.convert('L')
