import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

nltk.download('stopwords')
nltk.download('wordnet')

import re
from nltk.corpus import stopwords

def clean_text(text: str) -> str:
    stop_words = set(stopwords.words('english'))
    # remove punctuation and set to lower case
    text = re.sub(r'[^\w\s]', '', text.lower())
    cleaned_text = ' '.join([word for word in text.split() if word not in stop_words])
    return cleaned_text


def tokenize_text(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Tokenizes text in a specified column."""
    df[column] = df[column].apply(clean_text)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df[column])
    return pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
