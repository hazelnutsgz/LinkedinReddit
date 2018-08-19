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
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(chrome_options=chrome_options)



import pickle
import json

import re

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

    pattern = re.compile(r'/([a-zA-Z0-9-]+)')
    name = pattern.findall(url)[-1]
    with open(name + ".html", 'w') as fp:
        fp.write(driver.page_source)
    

    # education_list = driver.find_elements_by_css_selector("section#education-section li")
    # education_infos = []
    # for education_item in education_list:
    #     education_info = {}
    #     education_info["school_name"] = education_item.find_element_by_class_name("pv-entity__school-name").text
    #     education_info["degree"] = education_item.find_element_by_class_name("pv-entity__degree-name").find_element_by_class_name("pv-entity__comma-item").text
    #     education_info["major"] =  education_item.find_element_by_class_name("pv-entity__fos").find_element_by_class_name("pv-entity__comma-item").text
    #     times = education_item.find_element_by_class_name("pv-entity__dates").find_elements_by_tag_name("time")
    #     education_info["start"] = times[0].text
    #     education_info["end"] = times[1].text

    #     education_infos.append(education_info)
    # ret["education"] = education_infos

    work_infos = []
    work_list = driver.find_element_by_id("experience-section").find_elements_by_class_name("pv-position-entity")
    import pdb; pdb.set_trace()
    for work_item in work_list:
        try:
            temp = work_item.find_element_by_tag_name("ul")
            different_positions = temp.find_elements_by_tag_name("li")
            company = work_item.find_element_by_class_name("pv-entity__company-summary-info").find_element_by_tag_name("h3").find_elements_by_tag_name("span")[1].text
            for position in different_positions:
                work_info = {}
                work_info["company"] = company
                work_info["title"] = position.find_element_by_class_name("pv-entity__summary-info").find_elements_by_tag_name("span")[1].text
                work_info["duration"] = position.find_element_by_class_name("pv-entity__date-range").find_elements_by_tag_name("span")[1].text
                work_infos.append(work_info)
        except:
            work_info = {}
            ##Single position in one company
            work_info["title"] = work_item.find_element_by_class_name("pv-entity__summary-info").find_element_by_tag_name("h3").text
            work_info["company"] = work_item.find_element_by_class_name("pv-entity__secondary-title").text
            work_info["duration"] = work_item.find_element_by_class_name("pv-entity__date-range").find_elements_by_tag_name("span")[1].text 
            print (work_info)
            work_infos.append(work_info)
    ret["work"] = work_infos

    return ret

extract_information(driver, url)