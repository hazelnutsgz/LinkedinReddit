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
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import sys
import os

parentdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 #把目录加入环境变量
sys.path.insert(0,parentdir)


from login.linkedin_login import *


driver = get_driver()


print ("driver got??")
# driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")

result_dic = {}
# driver.get("https://www.linkedin.com/search/results/people/v2/?facetNetwork=%5B%22F%22%5D&facetSchool=%5B%2211319%22%5D&origin=FACETED_SEARCH")
with open("result_dict.json", "r") as fp:
    result_dic = json.loads(fp.read())




# driver.find_element_by_css_selector("a[data-control-name='search_with_filters']").click()
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
# print("Begin to srolling")
time.sleep(40)

while True:
	element = WebDriverWait(driver, 30, 0.5).until(ec.element_to_be_clickable((By.CSS_SELECTOR,"button.artdeco-pagination__button--next")))
	element_list = driver.find_elements_by_css_selector("a[data-control-name~='search_srp_result']")
	for item in element_list:
	    target_url = item.get_attribute("href")
	    if result_dict.get(target_url) == None:
	        print ("Add new the item")
	        result_dict[target_url] = True
	    else:
	    	print ("Duplicated")

	
	print("Current length is " + str(len(result_dict)))

	with open("error.html", 'w') as fp:
		fp.write(driver.page_source)

	with open("result_dict.json", "w") as fp:
		fp.write(json.dumps(result_dic))

	try:
		print ("click next........")
		driver.find_element_by_css_selector("button.artdeco-pagination__button--next").click()
		
		time.sleep(5)
		
		print("Begin to sroll.....")
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
	except Exception as e:
		print (e)
		time.sleep(10)











