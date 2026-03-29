import pandas as pd
import re

def clean_text(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z ]', '', text)

    return text


def clean_dataframe(df):

    df["clean_title"] = df["title"].apply(clean_text)

    return df