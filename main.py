import json
import time 

from scraper import Scraper
from page_scraper import scrape_url

def get_urls_from_file(filename: str) -> list:
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]
    
def save_results(results):
    with open('results.json', 'w') as f:
        json.dump(results, f, indent=4)

def main():
    start_time = time.time() 
    urls: list[str] = get_urls_from_file('urls.txt')
    scraper = Scraper(elements=urls, scrape_function=scrape_url, machine_cores=3, is_headless=False)
    scraper.scrape_all()
    end_time = time.time()
    duration = end_time - start_time
    print(f"Total scraping duration: {duration:.2f} seconds")
    print(f"Total scraped urls: {len(scraper.scraped_data)}")

    save_results(scraper.scraped_data)
    print("Saved results")
    
if __name__ == "__main__":
    main()
