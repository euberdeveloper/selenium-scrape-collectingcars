# selenium-scrape-collectingcars
A proof of concept repository to scrape details from the website collectingcars

## Usage

### Prerequisites

* Install [Pipenv](https://pipenv.pypa.io)
* Install Google Chrome Locally
* Clone this repository

### Procedure

* Install dependencies: `pipenv install`
* Run the script: `pipenv run scrape`
* The results will be saved in `results.json`

## Adjustments

* You can change the urls in the file `urls.txt`
* The `main.py` uses the `Scraper` class defined in `scraper.py`. You can adjust the parameters passed to the constructor:
    - elements: It is the list containing the "elements" that will define each scraping
    - scrape_function: It is the scraping function callback, that will receive the `driver`, `element` and the `index` of the element in the list as parameters
    - is_headless: It is a boolean that defines if the browser will be headless or not
    - machine_cores: It is the number of cores that will be used by the parallelization
* The `page_scraper.py` contains the scraping function, that will be run by the scraper. You can adjust the scraping functions to scrape the data you want
* The results of the scraping are in the `scraper.scraped_data` variable, that is a list of results returned by the callback


## Concepts

For each element, in this case url, a new browser will be opened. Tabs are not used, because this could produce problems with the cloudflare protection of the website to scrape. In addition, always for the same reason, `undetected-chromedriver` is used along with selenium. By using parallelization, the scraping is faster, this means that more than a browser will be launched in the same moment.