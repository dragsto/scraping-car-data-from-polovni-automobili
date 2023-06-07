## Scraping car data from polovni automobili
A little personal project that scrapes data from a car selling website www.polovniautomobili.com
The purpose is to gather data on used cars that include attributes such as vehicle name, price, year of manufacture, type of vehicle, km, and other specific car details.

This script can be run both locally on your computer or in a cloud-based Python notebook env like Google Colab.

### Dependencies

- requests
- BeautifulSoup 
- pandas
- random
- time
- urllib.parse
- sys

This script initiates by defining a base URL, which is the website from which data is to be scraped. It then creates an empty list, data, to hold the scraped information. It uses a set of headers to mimic a browser request, which is often necessary to avoid getting blocked by the website.

A for loop is initiated, which will iterate over a range of pages on the website. Within this loop, a GET request is sent to the website, and the HTML content is parsed using BeautifulSoup.

The script looks for all divs with the class 'textContentHolder' as these contain the information that we want to extract. Within these divs, it searches for certain HTML tags and classes that hold the car data.

The script Inline codehandles the possibility of request errors with a try/except block. It also introduces a delay between requests to avoid overloading the website server and getting blocked.

Once all the data has been extracted and stored in the data list, it's converted into a pandas DataFrame for easy manipulation and then saved to an Excel file named 'scraped_data.xlsx'.

> This script only fetches data from the first 50 pages of search results for demonstration purposes. You can modify the range() in the for loop to scrape more pages.

## How to use

### Local Environment

1. Install the necessary Python packages
2. Run the script
3. After the script has finished running, you should have an Excel file in the same directory named 'scraped_data.xlsx', which contains the scraped car data.

### Google Colab

1. Install the necessary Python packages
2. Copy and paste the script into a cell in the notebook and run the cell.
3. The scraped data will be saved as an Excel file in the Colab environment
