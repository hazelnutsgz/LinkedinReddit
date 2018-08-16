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

# driver.get("https://www.linkedin.com/") 
# driver.find_element_by_css_selector("input[name='session_key']").clear()
# driver.find_element_by_css_selector("input[name='session_key']").send_keys("m15201752137@163.com")
# driver.find_element_by_css_selector("input[name='session_password']").clear()
# driver.find_element_by_css_selector("input[name='session_password']").send_keys("#abcdefgh")
# driver.find_element_by_css_selector("input#login-submit").click()

# time.sleep(10)
# verification = input("Enter verification: ")
# s = None
# while not s:
#     try:
#         s = driver.find_element_by_id("verification-code")
#     except:
#         print ("Not ready yet")
#         continue

# s.send_keys(verification)
# driver.find_element_by_name("signin").click()

# time.sleep(10)

# import pickle

# try:
#     pickle.dump(driver.get_cookies() , open("cookies.pkl","wb"))
# except:
#     print ("Wrong about saving cookies")



with open("test.html", 'w') as fp:
    fp.write(driver.page_source)

driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")

# js="var q=document.documentElement.scrollTop="    
# distance = 10000
# offset = 10000 
result = []
counter = 0
while True:
    counter += 1
    element_list = driver.find_elements_by_class_name("search-result__result-link")
    for item in element_list:
        result.append(item.get_attribute("href"))
    
    print (result)
    if counter % 10 == 0:
        with open("result.json", "w") as fp:
            fp.write(json.dumps(result)) 

    try:
        driver.find_element_by_class_name("next").click()
    except:
        print ("Wrong with click")
        break

                           

