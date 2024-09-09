import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import datetime



def parse_immobilier_url_with_selenium(URL_rent_geneva_immobilier):
    """
    Load the immobilier URL with Selenium and return the soup object
    """
    # instantiate a Chrome options object. I can't just use the requests library because immobilier blocks it.
    # I understand that they don't want people scraping their website.
    options = webdriver.ChromeOptions()
    
    # set the options to use Chrome in headless mode
    options.add_argument("--headless=new")
    
    # initialize an instance of the Chrome driver (browser) in headless mode
    driver = webdriver.Chrome(options=options)
    
    # visit immobilier and get the page. 
    driver.get(URL_rent_geneva_immobilier)

    min_price_field = driver.find_element("id", "min-price-range")
    select = Select(min_price_field)
    select.select_by_visible_text("2600")

    # I need to click in certain fields to select my criteria, otherwise there are no apartments selected.



    # Then send it to beautiful soup for ease of parsing.
    soup = bs(driver.page_source, "html.parser")
    
    # release the resources allocated by Selenium and shut down the browser
    driver.quit()

    soup_str = str(soup.prettify())
    with open("immobilier.html", "w", encoding = "utf-8") as file:
        file.write(soup_str)

    elements = soup.find_all("div", {"class": "filter-item-container"})
    print(f"Found {len(elements)} elements with class 'filter-item-container'")

    for i, element in enumerate(elements):
        print(f"Element {i}: {element}")

    href_values = [element.find('a').get("href") for element in elements if element.find('a')]

    print(href_values)
    
    return soup

def parse_immobilier_url_without_selenium(URL_of_website):

    # Define the URL of the website
    url = URL_of_website

    # Set up headers to include a user-agent
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Make a GET request to the website with the headers
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response content with BeautifulSoup
        soup = bs(response.content, "html.parser")

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    
    elements = soup.find_all("div", {"class": "filter-item-container"})
    print(f"Found {len(elements)} elements with class 'filter-item-container'")

    for i, element in enumerate(elements):
        print(f"Element {i}: {element}")

    href_values = [element.find('a').get("href") for element in elements if element.find('a')]

    print(href_values)
    
    return