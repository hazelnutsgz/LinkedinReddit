import sys
import os
import requests
import json
import time
import numpy as np


parentdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from login.linkedin_login import *

driver = initial()
count = 0


with open("result_dict.json", "r") as fp:
    result = json.loads(fp.read())
result = [key for key in result]

while True:
	index = int(np.random.random() * 7000)
	url = result[index]
	trim_url = url.split('/')[-2]
	if os.path.exists("../html/" + trim_url + ".html") \
		or os.path.exists("../html/unlogin/" + trim_url + ".html"):
		print ("duplicated...")
		continue

	driver.get(url)
	content = driver.page_source
	if content.find("完整档案") != - 1:
		print (content)
		with open("../html/unlogin/" + trim_url + ".html", 'w') as fp:
			fp.write(content)
	else:
		print ("skipping")

	time.sleep(10000)



