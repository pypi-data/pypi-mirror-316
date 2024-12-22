import pandas as pd
import numpy as np

def remove_outliers(df: pd.DataFrame, column: str, threshold: float = 1.5) -> pd.DataFrame:
    """Removes outliers from a specified column using IQR."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
