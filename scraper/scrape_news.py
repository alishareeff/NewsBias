import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.bbc.com/news"

#Pretend to be a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

articles = []

headlines = soup.find_all(['h2', 'h3'])

for item in headlines:
    title = item.get_text().strip()
    
    # Filter out very short text (like "News", "Home", etc.)
    if len(title) > 10:
        articles.append({
            "source": "BBC",
            "title": title
        })

df = pd.DataFrame(articles).drop_duplicates()

df.to_csv("data/raw/bbc_news.csv", index=False)

print(f"Success! Found {len(df)} articles.")
print(df.head())