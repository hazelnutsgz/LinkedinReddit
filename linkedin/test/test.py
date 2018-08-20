import sys
sys.path.append("..")
from login.linkedin_login import get_driver
from parse.linkedin_profile import scrape_information


    

if __name__ == '__main__':
    driver = get_driver()
    scrape_information(driver, "https://www.linkedin.com/in/wei-hung-ko-088374110/")
    