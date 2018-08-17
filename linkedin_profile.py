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
    timeout = 10
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'background-details'))
        WebDriverWait(driver, timeout).until(element_present)
    except:
        print ("Timed out waiting for page to load")

    with open("test.html", 'w') as fp:
        fp.write(driver.page_source)
    

    education_list = driver.find_element_by_css_selector("section#education-section")
    print(education_list)
    education_infos = []
    for education_item in education_list:
        education_info = {}
        education_info["school_name"] = education_item.find_element_by_class_name("pv-entity__school-name").text()
        education_info["school_url"]
        education_info["degree"] = education_item.find_element_by_css_selector("#pv-entity__degree-name > #pv-entity__comma-item").text()
        education_info["major"] =  education_item.find_element_by_css_selector("#pv-entity__fos > #pv-entity__comma-item")
        time = education_item.find_element_by_css_selector("pv-entity__dates > time")
        import pdb; pdb.set_trace()

    ret["education"] = education_infos
    return ret

extract_information(driver, url)