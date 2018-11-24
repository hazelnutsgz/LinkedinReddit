import sys
import os
parentdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 #把目录加入环境变量
sys.path.insert(0,parentdir)

from login.linkedin_login import *


driver = get_driver("+8618018590368", "1f4542b9")


print ("driver got??")

with open("result_dict.json", "r") as fp:
    result = json.loads(fp.read())


time.sleep(40)		
count = 0
for url in result:
	trim_url = url.split('/')[-2]
	count += 1
	print (count)
	if os.path.exists("../html/" + trim_url + ".html") or\
		os.path.exists("../html/unlogin/" + trim_url + ".html"):
		print ("duplicated...")
		continue

	driver.get(url)
	time.sleep(5)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.5)")
	time.sleep(20)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
	time.sleep(20)
	
	if os.path.exists("../html/" + trim_url + ".html") or\
		os.path.exists("../html/unlogin/" + trim_url + ".html"):
		print ("duplicated...")
		continue

	with open("../html/" + trim_url + ".html", 'w') as fp:
		fp.write(driver.page_source)

	time.sleep(40)
	