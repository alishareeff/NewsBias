# NewsBias

Scrapes news headlines, scores them for sentiment, groups them by topic, and
visualises potential bias in a Streamlit dashboard.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the full pipeline
```bash
# 1. Scrape
python scraper/scrape_news.py

# 2. Clean + sentiment
python processing/cleaner.py
python processing/sentiment.py

# 3. Topic analysis + bias score
python analysis/topic_analysis.py

# 4. Dashboard
streamlit run dashboard/app.py
```

## Project layout

| Path | Purpose |
|---|---|
| `scraper/scrape_news.py` | Fetches BBC headlines via requests + BeautifulSoup |
| `processing/cleaner.py` | Lowercases and strips non-alpha characters |
| `processing/sentiment.py` | VADER compound score per headline |
| `analysis/topic_analysis.py` | LDA topic modelling + bias score |
| `embeddings/vector_index.py` | FAISS semantic search index |
| `dashboard/app.py` | Streamlit dashboard |
| `data/raw/` | Raw CSVs from scraper |
| `data/processed/` | Cleaned + enriched CSVs |

## Notes

- **Bias score** is `abs(sentiment)` — it measures emotional intensity, not
  political leaning. A score near 1 means strongly positive *or* strongly
  negative language; near 0 means neutral.
- The scraper currently targets BBC News. To add sources, duplicate
  `scrape_news.py` and change the URL + `"source"` field.