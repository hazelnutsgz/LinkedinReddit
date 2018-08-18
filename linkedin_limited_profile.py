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

# driver = webdriver.Chrome(chrome_options=chrome_options)
driver = webdriver.Firefox()


import pickle
import json
url = "https://www.linkedin.com/in/neema-mashayekhi-b5936129/"

driver.get("https://www.linkedin.com")
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
driver.implicitly_wait(100)
def extract_information(driver, url):
    driver.get(url)
    ret = {}
    js = "window.scrollTo(0, document.body.scrollHeight)"
    driver.execute_script(js)
    timeout = 15
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'background-details'))
        WebDriverWait(driver, timeout).until(element_present)
    except:
        print ("Timed out waiting for page to load")

    with open("test.html", 'w') as fp:
        fp.write(driver.page_source)

extract_information(driver, url)