# Tweets-Scrapper
## Dependencies Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install following
```bash
pip install -r requirements.txt
```

## Usage

Download it by clicking the green download button here on Github. You only need to parse argument specific Twitter keyword.
```python
>>> from twitter.tweety import tweets
>>> tweety = tweets('$BTC')
```

## Output

a CSV file containing: tweet +	time + sentiment + vader_compound +	vader_neg +	vader_neu +	vader_pos

![image](https://github.com/user-attachments/assets/c27c20c2-4859-437e-9d06-5d358f3c05c5)
