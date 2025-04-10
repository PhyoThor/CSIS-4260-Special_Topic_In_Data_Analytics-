# scrape_cnn_bing_bs4.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

start_time = time.time()
headers = {
    "User-Agent": "Mozilla/5.0"
}

results = []

# Each Bing page shows 10 results, so 10 pages = ~100 articles
for page in range(0, 100, 10):
    query = f"Nvidia site:cnn.com"
    url = f"https://www.bing.com/search?q={query}&first={page+1}"
    print(f"Scraping: {url}")

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    search_items = soup.find_all("li", class_="b_algo")

    for item in search_items:
        try:
            title = item.find("h2").text.strip()
            link = item.find("a")["href"]
            snippet_tag = item.find("p")
            snippet = snippet_tag.text.strip() if snippet_tag else ""

            results.append({
                "title": title,
                "url": link,
                "snippet": snippet
            })
        except Exception as e:
            print("Skipping item:", e)

    time.sleep(3)  # Polite delay

# Save results
df = pd.DataFrame(results)
df.to_csv("nvidia_cnn_bing.csv", index=False)

end_time = time.time()
duration = end_time - start_time
print(f" Saved {len(df)} CNN articles from Bing search")
print(f" Scraped {len(df)} CNN articles in {duration:.2f} seconds")
# The code above scrapes CNN articles about Nvidia from Bing search results using BeautifulSoup. 
# It saves the results to nvidia_cnn_bing.csv and prints the duration of the scraping process. 
# You can adjust the number of pages to scrape by changing the range in the for loop.