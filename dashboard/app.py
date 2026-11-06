import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="News Bias Analyzer", layout="wide")
st.title("News Bias Analyzer")

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/processed/articles.csv")

@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        return None
    return pd.read_csv(DATA_PATH)

df = load_data()

if df is None:
    st.warning("No processed data found. Run the scraper and processing pipeline first.")
    st.stop()

#Sidebar filters
st.sidebar.header("Filters")
sources = df["source"].unique().tolist() if "source" in df.columns else []
selected_sources = st.sidebar.multiselect("News source", sources, default=sources)
df = df[df["source"].isin(selected_sources)] if selected_sources else df

#KPI row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total articles", len(df))

if "sentiment" in df.columns:
    avg_sent = df["sentiment"].mean()
    col2.metric("Avg sentiment", f"{avg_sent:+.3f}")

if "bias_score" in df.columns:
    avg_bias = df["bias_score"].mean()
    label = "Low" if avg_bias < 0.2 else "Medium" if avg_bias < 0.5 else "High"
    col3.metric("Avg bias score", f"{avg_bias:.3f}", delta=label, delta_color="inverse")

if "topic" in df.columns:
    col4.metric("Topics detected", df["topic"].nunique())

st.divider()

#Charts
left, right = st.columns(2)

if "sentiment" in df.columns:
    with left:
        st.subheader("Sentiment distribution")
        fig = px.histogram(
            df, x="sentiment", nbins=30,
            color_discrete_sequence=["#4f8ef7"],
            labels={"sentiment": "Sentiment score"}
        )
        fig.update_layout(margin=dict(t=10, b=10), height=300)
        st.plotly_chart(fig, use_container_width=True)

if "topic" in df.columns and "bias_score" in df.columns:
    with right:
        st.subheader("Bias score by topic")
        topic_df = df.groupby("topic")["bias_score"].mean().reset_index()
        fig2 = px.bar(
            topic_df, x="topic", y="bias_score",
            color="bias_score",
            color_continuous_scale="RdYlGn_r",
            labels={"topic": "Topic", "bias_score": "Avg bias score"}
        )
        fig2.update_layout(margin=dict(t=10, b=10), height=300, coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

#Article table
st.subheader("Articles")
display_cols = [c for c in ["source", "title", "sentiment", "bias_score", "topic"] if c in df.columns]
sort_col = "bias_score" if "bias_score" in df.columns else None
st.dataframe(
    df[display_cols].sort_values(sort_col, ascending=False) if sort_col else df[display_cols],
    use_container_width=True,
    height=400
)
