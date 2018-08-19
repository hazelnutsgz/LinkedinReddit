import csv
import time
import json
import requests
from lxml import etree
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()

driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get("https://www.linkedin.com/") 
driver.find_element_by_css_selector("input[name='session_key']").clear()
driver.find_element_by_css_selector("input[name='session_key']").send_keys("m15201752137@163.com")
driver.find_element_by_css_selector("input[name='session_password']").clear()
driver.find_element_by_css_selector("input[name='session_password']").send_keys("#abcdefgh")
driver.find_element_by_css_selector("input#login-submit").click()

time.sleep(10)
verification = input("Enter verification: ")
s = None
while not s:
    try:
        s = driver.find_element_by_id("verification-code")
    except:
        print ("Not ready yet")
        continue

try:
    s.send_keys(verification)
    driver.find_element_by_name("signin").click()
except:
    pass




import pickle

try:
    pickle.dump(driver.get_cookies() , open("cookies.pkl","wb"))
except:
    print ("Wrong about saving cookies")

print ("Successfully saving the cookies")

import pickle

driver.get("https://www.linkedin.com")
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)

# driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
with open("test.html", 'w') as fp:
    fp.write(driver.page_source)



js = "window.scrollTo(0, document.body.scrollHeight)"
distance = 10000
offset = 10000 

result = []
batch = 10
while len(result) < 7000:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    element_list = driver.find_elements_by_class_name("mn-connection-card__link")
    result = []
    for item in element_list:
        result.append(item.get_attribute("href"))
    
    print("Current length is " + str(len(result)))
    with open("result_new.json", "w") as fp:
        fp.write(json.dumps(result)) 

                           

