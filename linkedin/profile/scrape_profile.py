import sys
import os
parentdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 #把目录加入环境变量
sys.path.insert(0,parentdir)

from login.linkedin_login import *
import requests

driver = get_driver()


print ("driver got??")

with open("result_dict.json", "r") as fp:
    result = json.loads(fp.read())

count = 0
for url in result:
	trim_url = url.split('/')[-2]
	if os.path.exists("../html/" + trim_url + ".html"):
		print ("duplicated...")
		continue


	driver.get(url)
	time.sleep(5)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.5)")
	time.sleep(5)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
	time.sleep(5)
	

	with open("../html/" + trim_url + ".html", 'w') as fp:
		fp.write(driver.page_source)


	print (count)
	time.sleep(2)
	count += 1