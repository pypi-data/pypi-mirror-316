import pandas as pd

def drop_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Drops rows with missing values."""
    return df.dropna()

def fill_missing(df: pd.DataFrame, value: float) -> pd.DataFrame:
    """Fills missing values with a specified value."""
    return df.fillna(value)
