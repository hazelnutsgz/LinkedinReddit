import json

new_dic = {}
with open("result_dict.json", 'r') as fp:
	dic = json.loads(fp.read())

count = 0
for url in dic:
	count += 1
	if count < 2000 or count > 5000:
		continue

	new_dic[url] = True


with open("result_dict.json", 'w') as fp:
	fp.write(json.dumps(new_dic))
