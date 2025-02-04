from tweets_scraper import tweets
from price_fetcher import gget_binance_data_by_requests
from stocktwits_scraper import scrape_stocktwits_posts

tweets_df = tweets('$BTC')
price_df = gget_binance_data_by_requests(ticker='BTCUSDT', interval='1m', start='2025-01-01 00:00:00', end='2025-02-01 00:00:00')
scrape_stocktwits_posts("BTC.X", max_posts=5)

print(price_df.head())
