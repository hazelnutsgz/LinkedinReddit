import sys
import os
import json
import argparse
from random import random

parentdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 #把目录加入环境变量
sys.path.insert(0,parentdir)
from login.linkedin_login import *

parser = argparse.ArgumentParser()
parser.add_argument("name")
parser.add_argument("start")
parser.add_argument("end")
args = parser.parse_args()

def func():
	with open("config.json") as fp:
		config = json.loads(fp.read())
	target = None
	for item in config:
		print (item["name"], args.name)
		if item["name"] == args.name:
			target = item
			break

	if target is None:
		print ("Can not find the account")
		return
	driver = get_driver(target["username"], \
		target["password"], os.path.join(target["position"], "cookies.pkl") )

	print ("driver got??")

	with open("result_dict.json", "r") as fp:
	    result = json.loads(fp.read())


	time.sleep(10)		
	count = 0
	for (url, judge) in result:
		trim_url = url.split('/')[-2]
		count += 1
		if count < int(args.start) or count > int(args.end):
			continue

		print (str(count) + ':', end='')
		if os.path.exists("html/" + trim_url + ".html"):
			print ("duplicated...")
			continue


		driver.get(url)
		if driver.page_source.find("Sign in to LinkedIn") != -1 or \
			driver.page_source.find("Don't have an account?") != -1:
			print("The account failed....")
			return

		for i in range(2):
			time.sleep(20*random())
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.5)")
			time.sleep(20*random())
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
			time.sleep(20*random())
		
		if os.path.exists("html/" + trim_url + ".html"):
			print ("duplicated...")
			continue

		with open("html/" + trim_url + ".html", 'w') as fp:
			fp.write(driver.page_source)
		print("success")
		time.sleep(70*random())


def clean():
	name_list = os.listdir("html")
	with open("result_dict.json", "r") as fp:
		result = json.loads(fp.read())
	
	for url in result:
		result[url] = "yes"
		for name in name_list:
			# import pdb; pdb.set_trace()
			if name.split('.')[0] == url.split('/')[-2]:
				result[url] = "no"
				break

	with open("result_dict.json", "w") as fp:
		fp.write(json.dumps(result))

def transfer():
	arr = []
	with open("result_dict.json", "r") as fp:
		result = json.loads(fp.read())

	for (key, val) in result.items():
		arr.append([key, val])

	with open("result_dict.json", "w") as fp:
		fp.write(json.dumps(arr))

if __name__ == '__main__':
	func()
	# clean()
	# transfer()

	