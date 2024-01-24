import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from joblib import Parallel, delayed
import multiprocessing

class Scraper:
    def __init__(self, elements: list, scrape_function, is_headless: bool = True, machine_cores: int = multiprocessing.cpu_count()):
        self.elements = elements
        self.is_headless = is_headless
        self.machine_cores = machine_cores
        self.scrape_function = scrape_function
        self.scraped_data = []

    def _get_driver(self):
        chrome_options = Options()
        if self.is_headless:
            chrome_options.add_argument("--headless")
        service = Service()
        driver = uc.Chrome(service=service, options=chrome_options)
        return driver

    def _scrape(self, index: int, element):
        driver = self._get_driver()
        try:
            print(f"[{index}] Scraping")
            scraped = self.scrape_function(driver, element, index)
            return scraped
        except Exception as e:
            print(f"[{index}] Error")
            print(e)
            return None
        finally:
            print(f"[{index}] Quitting")
            driver.quit()

    def scrape_all(self):
        with Parallel(n_jobs=self.machine_cores) as parallel:
            results = parallel(
                delayed(self._scrape)(index, element)
                for index, element in enumerate(self.elements))
            self.scraped_data = [result for result in results if result is not None]
