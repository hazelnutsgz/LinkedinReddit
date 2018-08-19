import csv
import time
import json
import requests
from lxml import etree
import lxml.cssselect
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pickle
import json

from login.linkedin_login import get_driver

import re

example_url = "https://www.linkedin.com/in/neema-mashayekhi-b5936129/"


def download_information(driver, url):
    driver.get("https://www.linkedin.com")

    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.get(url)
    ret = {}
    # js = "window.scrollTo(0, document.body.scrollHeight)"
    # driver.execute_script(js)
    timeout = 10
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'background-details'))
        WebDriverWait(driver, timeout).until(element_present)
    except:
        print ("Timed out waiting for page to load")

    pattern = re.compile(r'/([a-zA-Z0-9-]+)')
    name = pattern.findall(url)[-1] + '.html'
    with open(name, 'w') as fp:
        fp.write(driver.page_source)
    return name
    
def extract_information(filename):
    ret = {}
    with open(filename, 'r') as fp:
        target = etree.HTML(fp.read())
    ret["name"] = target.cssselect(".pv-top-card-section__name")[0].text
    education_list = target.cssselect("section#education-section li")
    education_infos = []
    for education_item in education_list:
        education_info = {}
        education_info["school_name"] = education_item.cssselect(".pv-entity__school-name")[0].text
        education_info["degree"] = education_item.cssselect(".pv-entity__degree-name")[0].cssselect(".pv-entity__comma-item")[0].text
        education_info["major"] =  education_item.cssselect(".pv-entity__fos")[0].cssselect(".pv-entity__comma-item")[0].text
        times = education_item.cssselect(".pv-entity__dates")[0].cssselect("time")
        education_info["start"] = times[0].text
        education_info["end"] = times[1].text

        education_infos.append(education_info)

    ret["education"] = education_infos
    import pdb; pdb.set_trace()
    work_infos = []
    work_list = target.cssselect("#experience-section")[0].cssselect(".pv-position-entity")
    for work_item in work_list:
        try:
            different_positions = work_item.cssselect("ul")[0].cssselect("li")
            company = work_item.cssselect(".pv-entity__company-summary-info")[0].cssselect("h3")[0].cssselect("span")[1].text
            
            for position in different_positions:
                work_info = {}
                work_info["company"] = company
                work_info["title"] = position.cssselect(".pv-entity__summary-info")[0].cssselect("span")[1].text
                work_info["duration"] = position.cssselect(".pv-entity__date-range")[0].cssselect("span")[1].text
                work_infos.append(work_info)
        except:
            work_info = {}
            ##Single position in one company
            import pdb; pdb.set_trace()
            work_info["title"] = work_item.cssselect(".pv-entity__summary-info")[0].cssselect("h3")[0].text
            work_info["company"] = work_item.cssselect(".pv-entity__secondary-title")[0].text
            work_info["duration"] = work_item.cssselect(".pv-entity__date-range")[0].cssselect("span")[1].text 
            print (work_info)
            work_infos.append(work_info)
    ret["work"] = work_infos
    with open(filename + ".json", 'w') as fp:
        fp.write(json.dumps(ret))

    return ret

def scrape_information(driver, url):
    name = download_information(driver, url)
    extract_information(name)

if __name__ == '__main__':
    driver = get_driver()
    scrape_information(driver, example_url)