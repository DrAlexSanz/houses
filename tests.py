import requests
from bs4 import BeautifulSoup
from houses_urls import URL_rent_geneva_immobilier

# Define the URL of the website
url = URL_rent_geneva_immobilier

# Set up headers to include a user-agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Make a GET request to the website with the headers
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Print the prettified HTML
    print(soup.prettify())
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")