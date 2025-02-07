from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
driver = webdriver.Edge()  
# hna khdit news li Hot f cryptopanic 
driver.get("https://cryptopanic.com/news?filter=hot")

## Sami hna rah khasek teb9a tscrolli f news 7ta tewsel lmax fin kaywli yreje3 bik l first ones
time.sleep(30)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

news_list = soup.find_all('div', class_='news-row news-row-link')

# 1000 posts to scrape
news_list = news_list[:1000]

# Open CSV file for writing
csv_filename = "cryptopanic_news.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    writer.writerow(["Time", "Title", "Source", "Votes"])

    # Extract news data and write to CSV
    for news in news_list:
        try:
            # Extract date
            time_tag = news.find('time')
            news_time = time_tag['datetime'] if time_tag else "N/A"

            # Extract titre
            title_tag = news.find('span', class_='title-text')
            news_title = title_tag.find('span').text.strip() if title_tag else "N/A"

            # Extract link source
            source_tag = news.find('span', class_='si-source-domain')
            source = source_tag.text.strip() if source_tag else "N/A"

            # Extract votes
            votes_section = news.find('div', class_='news-votes')
            votes = {}

            if votes_section:
                vote_spans = votes_section.find_all('span', class_='nc-vote-cont')
                for vote in vote_spans:
                    title_attr = vote.get('title', '')
                    if "votes" in title_attr:
                        key, value = title_attr.rsplit(" ", 1)
                        votes[key] = value.strip()

            votes_str = ", ".join([f"{key}: {value}" for key, value in votes.items()])

            # Write row to CSV
            writer.writerow([news_time, news_title, source, votes_str])

        except Exception as e:
            print(f"Error scraping a news item: {e}")

time.sleep(30)

driver.quit()

print(f"\n✅ Successfully scraped and saved 5 news articles to {csv_filename}!")
