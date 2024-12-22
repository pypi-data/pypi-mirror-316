import albumentations as A
import numpy as np

def augment_image(image: np.ndarray) -> np.ndarray:
    """Applies augmentation to the image."""
    transform = A.Compose([
        A.HorizontalFlip(p=0.5),  # Horizontal flip
        A.Affine(rotate=(-25, 25)),  # Rotate
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.0, p=0.5)  # Change brightness
    ])
    augmented = transform(image=image)
    return augmented['image']

def augment_batch(images: np.ndarray) -> np.ndarray:
    """Applies augmentation to a batch of images."""
    return np.array([augment_image(image) for image in images])
