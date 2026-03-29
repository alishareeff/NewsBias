import pandas as pd
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
from cleaner import clean_dataframe

sia = SentimentIntensityAnalyzer()

def get_sentiment(text):
    score = sia.polarity_scores(text)
    return score["compound"]

if __name__ == "__main__":
    df = pd.read_csv("data/raw/all_news.csv")
    df = clean_dataframe(df)
    df["sentiment"] = df["title"].apply(get_sentiment)
    df.to_csv("data/processed/articles.csv", index=False)
    print(f"Done! Saved {len(df)} articles with sentiment scores.")
    print(df[["title", "sentiment"]].head())