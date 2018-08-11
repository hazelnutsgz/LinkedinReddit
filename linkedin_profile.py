import csv
import time
import json
import requests
from lxml import etree
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

s = input("Enter verification: ")

print(type(s))


# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')

# driver = webdriver.Chrome(chrome_options=chrome_options)

# def scrape_all_connection(driver, url):
#     connection_url = url + 

