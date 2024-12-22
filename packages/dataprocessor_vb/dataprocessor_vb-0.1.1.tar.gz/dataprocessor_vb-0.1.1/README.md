# Data Tools Package

A comprehensive library for data preprocessing in AI development, focusing on scalability, usability, and modular design.

## Features

## Features

- **Data Loading**: Efficiently load datasets in various formats.
- **Data Cleaning**: Handle missing values, outliers, and duplicates.
- **Feature Engineering**: Create new features using advanced techniques.
- **Categorical Processing**: One-hot and label encoding for categorical variables.
- **Scaling**: Normalize and standardize numerical features.
- **Outlier Handling**: Detect and remove outliers using IQR.
- **Text Processing**: Clean, tokenize, and vectorize text data.
- **Time Series Processing**: Create time-based features and resample data.
- **Image Processing**: Load, resize, normalize, and convert images.
- **Image Augmentation**: Apply transformations to increase the diversity of your training dataset.

## usage

```py
from dataprocessor import DataLoader, DataCleaner, FeatureEngineer, ImageProcessor, ImageAugmenter

# Example usage of the package
loader = DataLoader()
data = loader.load_csv("data.csv")

cleaner = DataCleaner()
cleaned_data = cleaner.clean(data)

# Image processing example
image = ImageProcessor.load_image("path/to/image.jpg")
resized_image = ImageProcessor.resize_image(image, (224, 224))
normalized_image = ImageProcessor.normalize_image(resized_image)

# Image augmentation example
augmented_image = ImageAugmenter.augment_image(normalized_image)

```

## testing
```bash
poetry run pytest
```

# TODO:
- Fix file structure

# Package

[dataprocessor_vb pypi](https://pypi.org/project/dataprocessor_vb/)

1. configure pypi credentials if not already done
```bash
poetry config pypi-token.pypi <your-api-token>
```

2. publish the package
```bash
poetry publish --build
```

3. make also sure you add token to secrets under your repo settings in github

I think that the version should be updated manually, because now it updates the patch every commit.