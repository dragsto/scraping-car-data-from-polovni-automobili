import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
from urllib.parse import urlparse
import sys

#Define the base URL
base_url = "https://www.polovniautomobili.com/auto-oglasi/pretraga?page={}&sort=basic&city_distance=0&showOldNew=all&without_price=1"

#Define a list to store the scraped data
data = []

#Define headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

#Loop through the pages
for page in range(1, 50):
    sys.stdout.write(f"\rScraping page {page}...")
    sys.stdout.flush()
    for attempt in range(5):  # maximum 5 attempts
        try:
            #Send a GET request
            response = requests.get(base_url.format(page), headers=headers)

            #Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            #Find all divs with the class 'textContentHolder'
            divs = soup.find_all('div', class_='textContentHolder')

            #Loop through the divs and extract the data
            for div in divs:
                name = div.find('a', class_='ga-title')
                price = div.find('div', class_='price')

                top_details = div.find_all('div', class_='top')
                kilometers = ''
                year = ''
                type = ''
                for detail in top_details:
                    title = detail.get('title')
                    if title is not None:
                        if 'km' in title:
                            kilometers = detail.text.strip()
                        elif '.' in title:  # Assuming year will always have a dot.
                            year, type = detail.text.strip().split('.', 1)

                bottom_details = div.find('div', class_='bottom')
                hidden_details = div.find('div', class_='bottom uk-hidden-medium uk-hidden-small')

                if name and price and kilometers and year and type and bottom_details and hidden_details:
                    #Extract the link
                    parsed_url = urlparse(name['href'])
                    link = "https://www.polovniautomobili.com" + parsed_url.path

                    #Split the bottom details into two parts at the '|'
                    if '|' in bottom_details.text:
                        bottom_part1, bottom_part2 = bottom_details.text.split('|', 1)
                    else:
                        bottom_part1 = bottom_details.text
                        bottom_part2 = ''

                    data.append({
                        'Vozilo': name.text.strip(),
                        'Cena': price.text.strip(),
                        'Godina': year,
                        'Tip vozila': type.strip(),
                        'Kilometraza': kilometers,
                        'B/D': bottom_part1.strip(),
                        'Kubika': bottom_part2.strip(),
                        'KS': hidden_details.text.strip(),
                        'Link': link
                    })

            time.sleep(random.uniform(0.5, 1.2))
            break  #if the request was successful, break out of the loop
        except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError):
            if attempt < 4:  #if not the last attempt
                time.sleep(2**(attempt+1))  # exponential backoff
                continue
            else:
                raise

#Convert the list to a DataFrame
df = pd.DataFrame(data)

#Write the DataFrame to an Excel file
df.to_excel('scraped_data.xlsx', index=False)
