import csv
import time
import json
import requests
from lxml import etree
import lxml.cssselect
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pickle
import json
from functools import reduce

# from .. login.linkedin_login import get_driver

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
    try:
        ret["name"] = target.cssselect(".pv-top-card-section__name")[0].text
    except:
        ret["name"] = ''
    education_list = target.cssselect("section#education-section li")
    education_infos = []
    for education_item in education_list:
        education_info = {}
        try:
            education_info["school_name"] = education_item.cssselect(".pv-entity__school-name")[0].text
        except:
            education_info["school_name"] = ""
        try:
            education_info["degree"] = education_item.cssselect(".pv-entity__degree-name")[0].cssselect(".pv-entity__comma-item")[0].text
        except:
            education_info["degree"] = ""
        try:
            education_info["major"] = education_item.cssselect(".pv-entity__fos")[0].cssselect(".pv-entity__comma-item")[0].text
        except:
            education_info["major"] = ""
        try:
            times = education_item.cssselect(".pv-entity__dates")[0].cssselect("time")
        except:
            times = []
        try:
            education_info["start"] = times[0].text
        except:
            education_info["start"] = ""
        try:
            education_info["end"] = times[1].text
        except:
            education_info["end"] = ""
        education_infos.append(education_info)

    ret["education"] = education_infos
    work_infos = []
    different_positions = None
    work_list = None
    # import pdb; pdb.set_trace()
    try:
        work_list = target.cssselect("#experience-section")[0].cssselect(".pv-position-entity")
    except:
        work_list = []

    for work_item in work_list:
        try:
            ##Multiple position in one company
            
            different_positions = work_item.cssselect("ul")[0].cssselect("li")
            try:
                company = work_item.cssselect(".pv-entity__company-summary-info")[0].cssselect("h3")[0].cssselect("span")[1].text
            except:
                company = ""

            for position in different_positions:
                work_info = {}
                work_info["company"] = company
                work_info["title"] = position.cssselect(".pv-entity__summary-info")[0].cssselect("span")[1].text
                work_info["duration"] = position.cssselect(".pv-entity__date-range")[0].cssselect("span")[1].text
                work_infos.append(work_info)
        except:
            work_info = {}
            ##Single position in one company
            try:
                work_info["title"] = work_item.cssselect(".pv-entity__summary-info")[0].cssselect("h3")[0].text
            except:
                work_info["title"] = ""
            try:
                work_info["company"] = work_item.cssselect(".pv-entity__secondary-title")[0].text
            except:
                work_info["company"] = ""
            try:
                work_info["duration"] = work_item.cssselect(".pv-entity__date-range")[0].cssselect("span")[1].text 
            except:
                work_info["duration"] = ""
            work_infos.append(work_info)

    ret["work"] = work_infos


    if ret["name"] == '': 
        # or (ret["education"] == [] and ret["work"] == []):
        raise RuntimeError('NotFoundError')
    # import pdb;pdb.set_trace()
    if ret["education"] == []:
        ret["education"] = target.cssselect(".pv-top-card-v2-section__school-name")[0].text

    if ret["work"] == []:
        ret["work"] = target.cssselect(".pv-top-card-section__headline")[0].text

    try:
        ret["summary"] = ""
        str_lis = target.cssselect(".pv-top-card-section__summary")[0].cssselect("span")
        for str_item in str_lis:
            ret["summary"] += str_item.text
    except:
        # import pdb;pdb.set_trace()
        pass
    
    try:
        ret["connections"] = target.cssselect(".pv-top-card-v2-section__connections")[0].text
    except:
        pass

    print(ret)

    return ret


def clean_json(dic):
    for item in dic:
        item['connections'] = item['connections'][11:-9]
        item['name'] = item['name'][7:-5]
        if type(item['education']) is str:
            item['education'] = item['education'][2:-2]
        else:
            for education in item['education']:
                if "年" in education["start"]: 
                    education["start"] = education["start"][0:-2]
                if "年" in education["end"]: 
                    education["end"] = education["end"][0:-2]

    with open("parse.json", 'w') as fp:
        fp.write(json.dumps(dic, indent=4))

def scrape_information(driver, url):
    name = download_information(driver, url)
    extract_information(name)

def parse_all_info(directory):
    file_list = os.listdir(directory)
    count = 0
    error_list = []
    success = 0; fail = 0;
    ret = []
    for file in file_list:
        try:
            item = extract_information(
                os.path.join(directory, file))
            ret.append(item)
            success += 1
        except:
            error_list.append(file)
            fail += 1
        print(count)
        count += 1

    print("success:" + str(success))
    print("fail:" + str(fail))

    with open("error.log", 'w') as fp:
        fp.write(json.dumps(error_list))


    clean_json(ret)
    with open("parse.json", 'w') as fp:
        fp.write(json.dumps(ret))


if __name__ == '__main__':
    # driver = get_driver()
    # scrape_information(driver, example_url)
    parse_all_info("html")
    # extract_information(os.path.join("html", \
    #             "%E5%A8%81-%E5%88%98-629940132.html"))
    # with open("parse.json", 'r') as fp:
    #     target = fp.read()
    # clean_json(target)
    # with open("parse.json", 'w') as fp:
    #     fp.write(json.dumps(target))

