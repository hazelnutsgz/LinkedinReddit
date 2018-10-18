

import sys
import os
parentdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 #把目录加入环境变量
sys.path.insert(0,parentdir)


from login.linkedin_login import *


driver = get_driver()

driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
with open("test.html", 'w') as fp:
    fp.write(driver.page_source)



js = "window.scrollTo(0, document.body.scrollHeight)"
distance = 10000
offset = 10000 

result = []
batch = 10

with open("result.json", "r") as fp:
    result = json.loads(fp.read())

result_set = set(result)

# driver.find_element_by_css_selector("input[placeholder='Search by name']").send_keys("G")



driver.find_element_by_css_selector("div[data-control-name='sort_by_first_name']").click()
print("Set to click....")
time.sleep(10)

while len(result) < 100000:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    print("Begin to srolling")
    time.sleep(20)
    element_list = driver.find_elements_by_class_name("mn-connection-card__link")
    for item in element_list:
        target_url = item.get_attribute("href")
        if target_url not in result_set:
            print ("Add new the item")
            result_set.add(target_url)
        else:
        	print ("Duplicated")

    result_list = list(result_set)
    print("Current length is " + str(len(result_list)))

    

    with open("result.json", "w") as fp:
        fp.write(json.dumps(result_list))