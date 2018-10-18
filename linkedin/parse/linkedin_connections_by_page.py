import csv
import time
import json
import requests
from lxml import etree
from bs4 import BeautifulSoup
import pickle
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import sys
import os
parentdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 #把目录加入环境变量
sys.path.insert(0,parentdir)


from login.linkedin_login import *


driver = get_driver()

driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")

with open("result.json", "r") as fp:
    result = json.loads(fp.read())

result_set = set(result)


driver.find_element_by_css_selector("a[data-control-name='search_with_filters']").click()


count = 0
while True:
	element_list = driver.find_elements_by_css_selector("a[data-control-name~='search_srp_result']")
	print ("LLL")
	print (element_list)
	for item in element_list:
	    target_url = item.get_attribute("href")
	    if target_url not in result_set:
	        print ("Add new the item")
	        result_set.add(target_url)
	    else:
	    	print ("Duplicated")

	result_list = list(result_set)
	print("Current length is " + str(len(result_list)))

	with open(str(count) + ".html", 'w') as fp:
		fp.write(driver.page_source)
	count += 1

	driver.find_element_by_css_selector(".artdeco-pagination__button--next").click()
	print ("click next........")
	time.sleep(5)














