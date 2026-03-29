import streamlit as st
import pandas as pd

df = pd.read_csv("../data/processed/articles.csv")

st.title("News Bias Analyzer")

st.write(df)