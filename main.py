import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def scrape_seller_data(seller_urls):
    """
    Scrapes seller data from a list of URLs.
    """
    seller_data = []
    
    for url in seller_urls:
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                name = soup.select_one('.seller-name').text.strip() if soup.select_one('.seller-name') else "N/A"
                email = soup.select_one('.seller-email').text.strip() if soup.select_one('.seller-email') else "N/A"
                contact = soup.select_one('.seller-contact').text.strip() if soup.select_one('.seller-contact') else "N/A"
                location = soup.select_one('.seller-location').text.strip() if soup.select_one('.seller-location') else "N/A"
                categories = soup.select_one('.seller-categories').text.strip() if soup.select_one('.seller-categories') else "N/A"
                
                seller_data.append({
                    'Name': name,
                    'Email': email,
                    'Contact Number': contact,
                    'Location': location,
                    'Product Categories': categories,
                    'Profile URL': url
                })
            else:
                print(f"Failed to retrieve data from {url}. HTTP Status: {response.status_code}")
        except Exception as e:
            print(f"Error scraping {url}: {e}")
        time.sleep(random.uniform(1, 3))  # Introduce a delay to avoid getting blocked

    return seller_data

# Example URLs for testing
seller_urls = [
    "https://www.ebay.de/usr/example-seller1",
    "https://www.ebay.de/usr/example-seller2",
    "https://www.amazon.de/sp?seller=A12345678",
    "https://www.amazon.de/sp?seller=B98765432",
    "https://www.otto.de/haendler/example-seller1",
    "https://www.kaufland.de/haendler/example-seller2",
    "https://www.zalando.de/partner/example-seller1"
]

print("Starting data scraping...")
seller_data = scrape_seller_data(seller_urls)

if seller_data:
    df = pd.DataFrame(seller_data)
    df.to_csv('german_sellers_data_test.csv', index=False, encoding='utf-8')
    print("Data scraping completed. File saved as 'german_sellers_data_test.csv'.")
else:
    print("No seller data scraped. Check the URLs or selectors.")
