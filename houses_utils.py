import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs

def parse_immobilier_url_with_selenium(URL_rent_geneva_immobilier):
    """
    Load the immobilier URL with Selenium and return the soup object
    """
    # instantiate a Chrome options object. I can't just use the requests library because immobilier blocks it.
    # I understand that they don't want people scraping their website.
    options = Options()
    
    # set the options to use Chrome in headless mode
    options.add_argument("--headless=new")
    options.add_argument('--disable-notifications')
    
    # initialize an instance of the Chrome driver (browser) in headless mode
    driver = webdriver.Chrome(options=options)
    
    # visit immobilier and get the page. 
    driver.get(URL_rent_geneva_immobilier)

    # Wait for the input field to be visible and interactable
    wait = WebDriverWait(driver, 20)

    try:
        # Retry mechanism for the cookie consent dialog
        retries = 3
        for attempt in range(retries):
            try:
                cookie_consent_button = wait.until(EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")))
                cookie_consent_button.click()
                # Wait for the cookie consent dialog to disappear
                wait.until(EC.invisibility_of_element_located((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")))
                print("Cookie consent banner closed successfully.")
                break

            except Exception as e:
                print(f"Attempt {attempt + 1} to close cookie consent banner failed: {e}")

                if attempt < retries - 1:
                    driver.refresh()

                else:
                    raise Exception("Failed to close cookie consent banner after 3 attempts.")


        print("Passed the banner clicking")
        
        # Ensure the cookie consent dialog is closed
        wait.until(EC.invisibility_of_element_located((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")))

        # Wait for the price dropdown button to be clickable and click it to open the dropdown
        price_button = wait.until(EC.element_to_be_clickable((By.ID, "priceLabel")))
        print("dropdown is visible")
        
        # Scroll to the button to ensure it is within the viewport
        driver.execute_script("arguments[0].scrollIntoView();", price_button)
        
        # Retry clicking the button if intercepted
        retries = 3
        for attempt in range(retries):

            try:
                price_button.click()
                print("Price dropdown button clicked successfully.")
                break

            except Exception as e:
                print(f"Attempt {attempt + 1} to click price dropdown button failed: {e}")
                wait.until(EC.element_to_be_clickable((By.ID, "priceLabel")))

        # Wait for the dropdown menu to become visible
        dropdown_menu = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "dropdown__menu")))
        
        # Locate the list item with the value 2600 and click it
        min_price_option = dropdown_menu.find_element(By.XPATH, "//li[@data-range-min-value='2600']")
        min_price_option.click()
        print("Minimum price option 2600 clicked successfully.")

        # I need to click in certain fields to select my criteria, otherwise there are no apartments selected.

        # Then send it to beautiful soup for ease of parsing.
        soup = bs(driver.page_source, "html.parser")
        return soup

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser
        driver.quit()

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