from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os
import csv
from dotenv import load_dotenv

def scrape_stocktwits_posts(stock_name, max_posts=10):
    driver = webdriver.Chrome()

    driver.get("https://stocktwits.com/signin")

    # Load login credentials from .env file
    load_dotenv()

    wait = WebDriverWait(driver, 10)
    email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-testid="log-in-username"]')))
    email_input.send_keys(os.getenv("stocktwits_email"))

    password_input = driver.find_element(By.CSS_SELECTOR, 'input[data-testid="log-in-password"]')
    password_input.send_keys(os.getenv("stocktwits_pswd"))

    sign_in_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="log-in-submit"]')
    sign_in_button.click()

    time.sleep(5)

    driver.get(f"https://stocktwits.com/symbol/{stock_name}")
    time.sleep(5)

    def scroll_to_load_posts(driver, max_posts):
        posts_data = []  
        previous_count = 0

        while len(posts_data) < max_posts:
            post_messages = driver.find_elements(By.CSS_SELECTOR, 'div.RichTextMessage_body__4qUeP.whitespace-pre-wrap')
            timestamps = driver.find_elements(By.CSS_SELECTOR, 'time.StreamMessage_timestamp__VVDmF')
            min_length = min(len(post_messages), len(timestamps))

            if len(post_messages) == previous_count:
                print("No more posts are loading. Exiting.")
                break

            for i in range(previous_count, min_length):
                post_text = post_messages[i].text
                post_time = timestamps[i].get_attribute("datetime") if i < len(timestamps) else "Unknown"

                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", post_messages[i])
                time.sleep(1) 

                posts_data.append((post_text, post_time))

                if len(posts_data) >= max_posts:
                    break
            
            previous_count = len(post_messages)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        return posts_data

    posts_data = scroll_to_load_posts(driver, max_posts)

    # Save to CSV
    with open(f"stockTwits_posts_{stock_name}.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Post Number", "Post Text", "Post Date"])  
        for i, (text, date) in enumerate(posts_data, 1):
            writer.writerow([i, text, date])

    time.sleep(5)
    driver.quit()
