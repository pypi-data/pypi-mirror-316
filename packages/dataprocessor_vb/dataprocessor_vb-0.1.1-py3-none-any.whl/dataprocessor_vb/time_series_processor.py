import pandas as pd

def create_time_features(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    """Creates time-based features from a date column."""
    df[date_column] = pd.to_datetime(df[date_column])
    df['year'] = df[date_column].dt.year
    df['month'] = df[date_column].dt.month
    df['day'] = df[date_column].dt.day
    df['weekday'] = df[date_column].dt.weekday
    return df

def resample_time_series(df: pd.DataFrame, date_column: str, frequency: str) -> pd.DataFrame:
    """Resamples the time series data."""
    df.set_index(date_column, inplace=True)
    return df.resample(frequency).mean().reset_index()
