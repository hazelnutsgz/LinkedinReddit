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
import pickle
from selenium.webdriver.remote.webdriver import WebDriver

def initial():
    chrome_options = Options()
    # chrome_options.add_argument("--disable-web-security");
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver



def login(driver, username, passwd, cookie_file):
    print ("Try to login..........")
    driver.get("https://www.linkedin.com/") 
    driver.find_element_by_css_selector("input[name='session_key']").clear()
    # driver.find_element_by_css_selector("input[name='session_key']").send_keys("m15201752137@163.com")
    # driver.find_element_by_css_selector("input[name='session_password']").clear()
    # driver.find_element_by_css_selector("input[name='session_password']").send_keys("#abcdefgh")
    
    driver.find_element_by_css_selector("input[name='session_key']").send_keys(username)
    driver.find_element_by_css_selector("input[name='session_password']").clear()
    driver.find_element_by_css_selector("input[name='session_password']").send_keys(passwd)


    driver.find_element_by_css_selector("input#login-submit").click()

    time.sleep(5)
    ##If need verification
    try:
        s = driver.find_element_by_id("verification-code")
        verification = input("Enter verification: ")
        s.send_keys(verification)
        driver.find_element_by_name("signin").click()
    except:
        ##Check wheter need graphic authentication
        pass        

    try:
        pickle.dump(driver.get_cookies() , open(cookie_file,"wb"))
    except:
        print ("Wrong about saving cookies")

    print ("Successfully saving the cookies")
    return driver



def get_driver(username, passwd, cookie_file):
    driver = initial()
    driver.get("https://www.linkedin.com")
    try:
        cookies = pickle.load(open(cookie_file, "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
    except:
        return login(driver, username, passwd, cookie_file)

    driver.get("https://www.linkedin.com")  
    time.sleep(3)
    if driver.page_source.find("Guozhen She") == 0:
        print ("Need login")
        return login(driver, username, passwd, cookie_file)
    
    with open("welcomepage.html", 'w') as fp:
        fp.write(driver.page_source)

    return driver
 


def attach_to_session(executor_url, session_id):
    original_execute = WebDriver.execute
    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return original_execute(self, command, params)
    # Patch the function before creating the driver object
    WebDriver.execute = new_command_execute
    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    driver.session_id = session_id
    # Replace the patched function with original function
    WebDriver.execute = original_execute
    return driver

                           

