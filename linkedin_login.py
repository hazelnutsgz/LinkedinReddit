import csv
import time
import json
import requests
from lxml import etree
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get("https://www.linkedin.com/") 
driver.find_element_by_css_selector("input[name='session_key']").clear()
driver.find_element_by_css_selector("input[name='session_key']").send_keys("m15201752137@163.com")
driver.find_element_by_css_selector("input[name='session_password']").clear()
driver.find_element_by_css_selector("input[name='session_password']").send_keys("#abcdefgh")
driver.find_element_by_css_selector("input#login-submit").click()


driver.get("https://www.linkedin.com/")
print(driver.page_source)


