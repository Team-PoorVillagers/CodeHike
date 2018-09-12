import requests
import json
import pickle
import csv
import time 
def pretty(file):
	return json.dumps(parse , indent = 4)

access_token = "8ffc87dc7701a8f0c3b1157413e0f36dad7bb314"

headers = {
	'content-type' : 'application/json',
	'Authorization' : 'Bearer {}'.format(access_token)	

}


main_list = []
heading = []
flag = 0
	
i = 1
while(1):
	print(i)
	url = 'https://api.codechef.com/submissions/?contestCode=COOK95A&offset='+str(i)+'&limit=100'
	i += 20
	a = requests.get(url=url,headers=headers)
	parsed = a.json()

	# print(json.dumps(parsed, indent=4))	


	try:
		for j in parsed["result"]["data"]["content"]:
			lis = []
			# print(j)
			for key in j:
				if flag == 0:
					heading.append(key)
				lis.append(j[key])
			if flag == 0:
				main_list.append(heading)
			flag = 1
			main_list.append(lis)
	except:
		break


	time.sleep(11)


myFile = open('out.csv', 'a')
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(main_list)
