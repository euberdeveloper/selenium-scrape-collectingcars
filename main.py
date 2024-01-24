import datetime 
import pandas as pd

from scraper import Scraper
from cronometer import Cronometer
from page_scraper import scrape_url

def get_urls_from_file(filename: str) -> list:
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]
    
def save_results(results):
    current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = (f'./results_{current_datetime}.xlsx')
    result_df = pd.DataFrame(results)
    result_df.to_excel(output_filename, index=False)

def main():
    cronometer = Cronometer()
    cronometer.start()

    urls: list[str] = get_urls_from_file('urls.txt')
    scraper = Scraper(elements=urls, scrape_function=scrape_url, machine_cores=2, is_headless=False)
    scraper.scrape_all()
    
    cronometer.stop()
    cronometer.print()
    print(f"Total scraped urls: {len(scraper.scraped_data)}")

    save_results(scraper.scraped_data)
    print("Saved results")
    
if __name__ == "__main__":
    main()
