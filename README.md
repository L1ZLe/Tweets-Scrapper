---

# Tweets-Scrapper

A Python-based tool for scraping tweets related to specific keywords, analyzing their sentiment, and saving the results to a CSV file.

## Dependencies Installation

To get started, you'll need to install the required dependencies. Use [pip](https://pip.pypa.io/en/stable/) to install all dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Usage

To use the scraper, download the project from GitHub (click the green "Code" button and then "Download ZIP"). After extracting the files, you can easily parse a specific Twitter keyword by running the following Python code:

```python
>>> from twitter.tweety import tweets
>>> tweety = tweets('$BTC')  # Replace '$BTC' with any keyword you're interested in
```

## Output

The scraper will generate a CSV file containing the following information for each tweet:

- **tweet**: The text of the tweet
- **time**: Timestamp of the tweet
- **sentiment**: Sentiment polarity (positive, neutral, or negative)
- **vader_compound**: Compound score calculated by VADER sentiment analysis
- **vader_neg**: VADER negative sentiment score
- **vader_neu**: VADER neutral sentiment score
- **vader_pos**: VADER positive sentiment score

### Sample CSV Format:

| tweet                                  | time                | sentiment | vader_compound | vader_neg | vader_neu | vader_pos |
|----------------------------------------|---------------------|-----------|----------------|-----------|-----------|-----------|
| Bitcoin is skyrocketing! #BTC          | 2025-02-03 12:34:56 | Positive  | 0.75           | 0.10      | 0.20      | 0.70      |
| Cryptocurrency market is volatile...   | 2025-02-03 12:45:01 | Negative  | -0.60          | 0.30      | 0.60      | 0.10      |
| The future of digital assets is here.  | 2025-02-03 13:01:45 | Neutral   | 0.05           | 0.05      | 0.90      | 0.05      |

![Screenshot](https://github.com/user-attachments/assets/c27c20c2-4859-437e-9d06-5d358f3c05c5)

## Tested Using

- Chromium version: `132.0.6834.159`
- Platform: Debian GNU/Linux 12 (Bookworm)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

