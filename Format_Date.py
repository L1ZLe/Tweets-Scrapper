import pandas as pd
from datetime import datetime

# Load the CSV file
file_path = "cryptopanic_news.csv"  
df = pd.read_csv(file_path)

# Function to extract date and time
def split_datetime(timestamp):
    try:
        dt = datetime.strptime(timestamp[:24], "%a %b %d %Y %H:%M:%S")
        return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M:%S")
    except ValueError:
        return None, None

df["Date"], df["Time"] = zip(*df["Time"].apply(split_datetime))

df = df[["Date", "Time", "Title", "Source", "Votes"]]

new_file_path = "cryptopanic_news_updated.csv"
df.to_csv(new_file_path, index=False)

print(f"Updated file saved as: {new_file_path}")
