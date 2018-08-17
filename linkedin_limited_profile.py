import csv
import time
import json
import requests
from lxml import etree
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(chrome_options=chrome_options)



import pickle
import json
url = "https://www.linkedin.com/in/neema-mashayekhi-b5936129/"


def extract_information(driver, url):
    driver.get(url)
    ret = {}

    with open("test.html", 'w') as fp:
        fp.write(driver.page_source)
        
    ret["name"] = driver.find_element_by_css_selector("#profile-overview-content h1").text()
    ret["connections"] = driver.find_element_by_css_selector("#member-connections strong").text()
    ret["positions"] = []
    s = driver.find_element_by_css_selector("ul#positions") 
    print(s)

if __name__ == '__main__':
    extract_information(driver, url)