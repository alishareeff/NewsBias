import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

N_TOPICS = 5
N_TOP_WORDS = 8

def get_top_words(model, feature_names, n=N_TOP_WORDS):
    topics = {}
    for i, topic in enumerate(model.components_):
        top = [feature_names[j] for j in topic.argsort()[:-n - 1:-1]]
        topics[f"topic_{i}"] = top
    return topics

def assign_topic(text, vectorizer, model):
    vec = vectorizer.transform([text])
    dist = model.transform(vec)[0]
    return int(dist.argmax())

def run_topic_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Fit LDA on clean_title and add topic + bias_score columns."""
    texts = df["clean_title"].fillna("").tolist()

    vectorizer = CountVectorizer(max_df=0.9, min_df=2, stop_words="english")
    dtm = vectorizer.fit_transform(texts)

    lda = LatentDirichletAllocation(
        n_components=N_TOPICS,
        random_state=42,
        max_iter=10
    )
    lda.fit(dtm)

    df["topic"] = df["clean_title"].apply(
        lambda t: assign_topic(t, vectorizer, lda)
    )

    # Bias score: absolute value of sentiment — 0 = neutral, 1 = strongly toned
    if "sentiment" in df.columns:
        df["bias_score"] = df["sentiment"].abs()
    else:
        df["bias_score"] = 0.0

    top_words = get_top_words(lda, vectorizer.get_feature_names_out())
    print("Discovered topics:")
    for k, v in top_words.items():
        print(f"  {k}: {', '.join(v)}")

    return df, top_words


if __name__ == "__main__":
    df = pd.read_csv("data/processed/articles.csv")
    df, topics = run_topic_analysis(df)
    df.to_csv("data/processed/articles.csv", index=False)
    print(df[["title", "topic", "bias_score"]].head(10))