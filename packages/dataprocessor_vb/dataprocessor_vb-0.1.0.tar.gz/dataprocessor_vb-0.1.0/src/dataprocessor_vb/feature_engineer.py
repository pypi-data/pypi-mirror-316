import pandas as pd

def create_age_feature(df: pd.DataFrame, birth_col: str) -> pd.DataFrame:
    """Creates an 'age' feature from a birthdate column."""
    df['age'] = pd.to_datetime('today').year - pd.to_datetime(df[birth_col]).dt.year
    return df
