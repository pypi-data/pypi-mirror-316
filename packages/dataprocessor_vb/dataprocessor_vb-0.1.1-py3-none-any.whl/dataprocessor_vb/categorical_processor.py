import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

def one_hot_encode(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Performs one-hot encoding on a specified column."""
    encoder = OneHotEncoder(sparse_output=False)
    encoded_features = encoder.fit_transform(df[[column]])
    encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out([column]))
    return df.join(encoded_df).drop(columns=[column])

def label_encode(df: pd.DataFrame, column: str) -> pd.Series:
    """Performs label encoding on a specified column."""
    encoder = LabelEncoder()
    return encoder.fit_transform(df[column])
