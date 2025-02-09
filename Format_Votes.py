import pandas as pd
import re

# Load the CSV file
file_path = "cryptopanic_news_updated.csv"  
df = pd.read_csv(file_path)

def extract_votes(vote_string, vote_type):
    match = re.search(rf"(\d+)\s+{vote_type}", str(vote_string))
    return int(match.group(1)) if match else 0

df["Positive Votes"] = df["Votes"].apply(lambda x: extract_votes(x, "positive"))
df["Important Votes"] = df["Votes"].apply(lambda x: extract_votes(x, "important"))
df["Negative Votes"] = df["Votes"].apply(lambda x: extract_votes(x, "negative"))
df["Like Votes"] = df["Votes"].apply(lambda x: extract_votes(x, "like"))
df["Dislike Votes"] = df["Votes"].apply(lambda x: extract_votes(x, "dislike"))
df["Saves Votes"] = df["Votes"].apply(lambda x: extract_votes(x, "saves"))
df["lol Votes"] = df["Votes"].apply(lambda x: extract_votes(x, "lol"))
df["Comments Votes"] = df["Votes"].apply(lambda x: extract_votes(x, "comments"))

# Drop the original "Votes" column and reorder columns
df = df[["Date", "Time", "Title", "Source", "Positive Votes", "Important Votes", "Negative Votes", "Comments Votes", "Like Votes", "Dislike Votes", "Saves Votes", "lol Votes"]]

new_file_path = "cryptopanic_news_final.csv"
df.to_csv(new_file_path, index=False)

print(f"Updated file saved as: {new_file_path}")
