import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

SOURCES = {
    "BBC": {
        "url": "https://www.bbc.com/news",
        "tags": ["h2", "h3"],
    },
    "CNN": {
        "url": "https://www.cnn.com",
        "tags": ["h2", "h3"],
    },
    "AlJazeera": {
        "url": "https://www.aljazeera.com",
        "tags": ["h2", "h3"],
    },
    "TheGuardian": {
        "url": "https://www.theguardian.com",
        "tags": ["h2", "h3"],
    },
}

os.makedirs("data/raw", exist_ok=True)

def scrape_source(name, config):
    print(f"Scraping {name}...")
    try:
        response = requests.get(config["url"], headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []
        for tag in config["tags"]:
            for item in soup.find_all(tag):
                title = item.get_text().strip()
                if len(title) > 10:
                    articles.append({"source": name, "title": title})
        df = pd.DataFrame(articles).drop_duplicates()
        path = f"data/raw/{name.lower()}_news.csv"
        df.to_csv(path, index=False)
        print(f"  ✓ {len(df)} articles saved to {path}")
        return df
    except Exception as e:
        print(f"  ✗ Failed to scrape {name}: {e}")
        return pd.DataFrame()


if __name__ == "__main__":
    all_frames = []
    for name, config in SOURCES.items():
        df = scrape_source(name, config)
        all_frames.append(df)

    combined = pd.concat(all_frames, ignore_index=True).drop_duplicates()
    combined.to_csv("data/raw/all_news.csv", index=False)
    print(f"\nDone! {len(combined)} total articles across all sources.")
    print(combined["source"].value_counts().to_string())