import pandas as pd

def load_csv(file_path: str) -> pd.DataFrame:
    """Loads a CSV file into a DataFrame."""
    return pd.read_csv(file_path)

def load_json(file_path: str) -> pd.DataFrame:
    """Loads a JSON file into a DataFrame."""
    return pd.read_json(file_path)
