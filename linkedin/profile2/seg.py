import json

new_dic = {}
with open("result_dict.json", 'r') as fp:
	dic = json.loads(fp.read())

count = 0
for url in dic:
	if count < 7000:
		count += 1
	new_dic[url] = True


with open("result_dict1.json", 'w') as fp:
	fp.write(json.dumps(new_dic))
