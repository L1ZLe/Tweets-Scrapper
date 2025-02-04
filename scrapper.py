from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from textblob import TextBlob
from bs4 import BeautifulSoup
from datetime import datetime
import chromedriver_binary
from requests import get
import pandas as pd
import time, sys, re, os
from selenium.webdriver.common.by import By
# from openai import OpenAI  # Commented out
from dotenv import load_dotenv

class tweets:
    """
    Collects tweets with timestamps from Twitter based on a keyword/hashtag.
    Includes both tweet text, publication time, and engagement metrics.
    """

    def __init__(self, keyword):
        # Load environment variables
        load_dotenv()
        # api_key_deepseek = os.getenv("api_key_deepseek")  # Commented out

        # if not api_key_deepseek:
        #     raise ValueError("API key for DeepSeek not found in environment variables.")

        start_time = datetime.now()

        # Initialize DeepSeek client (commented out)
        # self.client = OpenAI(
        #     base_url="https://openrouter.ai/api/v1",
        #     api_key=api_key_deepseek
        # )

        # Configure Chrome options
        options = Options()
        options.headless = False  # Disable headless for debugging
        browser = webdriver.Chrome(options=options)

        # Load Twitter search
        browser.get(f"https://twitter.com/search?q={keyword}&src=typed_query")

        # Wait for initial content to load
        try:
            WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]'))
            )
        except Exception as e:
            print("Timeout waiting for initial tweets to load")
            browser.quit()
            return

        # Scroll and collect tweets
        last_height = browser.execute_script("return document.body.scrollHeight")
        tweets_set = set()

        while (datetime.now() - start_time).seconds < 60:  # 1-minute collection
            # Scroll down
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for content to load

            # Find new tweets using Selenium
            new_tweets = browser.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
            for tweet in new_tweets:
                try:
                    # Extract tweet text
                    text_element = tweet.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                    text = text_element.text

                    # Extract timestamp
                    time_element = tweet.find_element(By.TAG_NAME, 'time')
                    timestamp = time_element.get_attribute('datetime')

                    # Extract engagement metrics
                    def get_count(tweet_element, testid):
                        try:
                            element = tweet_element.find_element(By.CSS_SELECTOR, f'[data-testid="{testid}"]')
                            aria_label = element.get_attribute('aria-label')
                            return int(''.join(filter(str.isdigit, aria_label))) if aria_label else 0
                        except:
                            return 0

                    replies = get_count(tweet, "reply")
                    retweets = get_count(tweet, "retweet")
                    likes = get_count(tweet, "like")

                    tweets_set.add((text, timestamp, replies, retweets, likes))
                except Exception as e:
                    print(f"Error extracting tweet: {str(e)}")
                    continue

            # Check scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        browser.quit()

        # Process collected tweets
        self.tweets = [{"text": t[0], "time": t[1], 
                       "replies": t[2], "retweets": t[3], "likes": t[4]} 
                      for t in tweets_set]
        print(f"Collected {len(self.tweets)} tweets")

        if not self.tweets:
            print("No tweets collected. Check selectors or login requirements.")
            return

        # Sentiment analysis
        analyser = SentimentIntensityAnalyzer()
        sentiment_data = []

        for tweet in self.tweets:
            clean_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet['text']).split())

            # VADER Sentiment
            vader_scores = analyser.polarity_scores(clean_tweet)

            # TextBlob Sentiment
            analysis = TextBlob(clean_tweet)
            if analysis.sentiment.polarity > 0:
                sentiment = 'positive'
            elif analysis.sentiment.polarity == 0:
                sentiment = 'neutral'
            else:
                sentiment = 'negative'

            # Add to sentiment data
            sentiment_data.append({
                'tweet': clean_tweet,
                'time': tweet['time'],
                'replies': tweet['replies'],
                'retweets': tweet['retweets'],
                'likes': tweet['likes'],
                'sentiment': sentiment,
                'vader_compound': vader_scores['compound'],
                'vader_neg': vader_scores['neg'],
                'vader_neu': vader_scores['neu'],
                'vader_pos': vader_scores['pos']
            })

        self.tweets_df = pd.DataFrame(sentiment_data)

        if not self.tweets_df.empty:
            # Convert ISO time to readable format
            self.tweets_df['time'] = pd.to_datetime(self.tweets_df['time']).dt.strftime('%Y-%m-%d %H:%M:%S')
            self.tweets_df.to_csv('tweets.csv', index=False)
            print("Tweets saved to 'tweets.csv'")
        else:
            print("No tweets to save")
