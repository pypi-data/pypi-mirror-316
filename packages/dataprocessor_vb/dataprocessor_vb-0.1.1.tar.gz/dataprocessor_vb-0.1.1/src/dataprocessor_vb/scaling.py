import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def standardize(df: pd.DataFrame) -> pd.DataFrame:
    """Standardizes features by removing the mean and scaling to unit variance."""
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)
    return pd.DataFrame(scaled_data, columns=df.columns)

def normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Normalizes features to a range of [0, 1]."""
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(df)
    return pd.DataFrame(normalized_data, columns=df.columns)
