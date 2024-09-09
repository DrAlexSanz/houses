# As usual, this is the main file and the functions are in houses_utils.py

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import datetime

# Import the functions from the houses_utils file
from houses_utils import parse_immobilier_url_without_selenium, parse_immobilier_url_with_selenium

# Import the URLs from the urls file

from houses_urls import URL_rent_geneva_immobilier

parse_immobilier_url_with_selenium(URL_rent_geneva_immobilier)

print("Finished script")