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


def initial():
    chrome_options = Options()
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver


def login(driver):

    driver.get("https://www.linkedin.com/") 
    driver.find_element_by_css_selector("input[name='session_key']").clear()
    driver.find_element_by_css_selector("input[name='session_key']").send_keys("m15201752137@163.com")
    driver.find_element_by_css_selector("input[name='session_password']").clear()
    driver.find_element_by_css_selector("input[name='session_password']").send_keys("#abcdefgh")
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
        pickle.dump(driver.get_cookies() , open("cookies.pkl","wb"))
    except:
        print ("Wrong about saving cookies")

    print ("Successfully saving the cookies")
    return driver



import pickle


def get_driver():
    driver = initial()
    driver.get("https://www.linkedin.com")
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://www.linkedin.com")  
    try:
        driver.find_element_by_class_name("link-forgot-password")
        return login(driver)
    except:
        return driver
    
 

                           

