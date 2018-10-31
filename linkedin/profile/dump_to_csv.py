import pandas as pd
import json
import os
with open("result_dict.json", "r") as fp:
    result = json.loads(fp.read())


count = 0
lis = []
for url in result:
	trim_url = url.split('/')[-2]
	if os.path.exists("../html/" + trim_url + ".html") or\
		os.path.exists("../html/unlogin/" + trim_url + ".html"):
		print ("duplicated...")
		continue
	lis.append(url)

dit = {'A': lis}
df = pd.DataFrame(dit)

df.to_csv('./result.csv',columns=['A'],index=False,sep=',')