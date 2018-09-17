import requests
import json
import datetime

import csv


import credentials as cred_file

from global_app_details import client_id, client_secret, redirect_uri




headers = {
	'content-type': 'application/json',
	'Authorization': 'Bearer {}'.format(cred_file.access_token)
}

def activate_access_token():
	if(cred_file.generated_on != ""):
		fmt = '%Y-%m-%d %H:%M:%S.%f'
		tstamp1 = datetime.datetime.strptime(cred_file.generated_on, fmt)
		tstamp2 = datetime.datetime.now()
		diff = tstamp2 - tstamp1
		# x = seconds since access token generated
		x = diff.total_seconds()
		# given access token expires in 3600 seconds, taking 3000 as limit 
		if(int(x) > 3000):
			get_access_token()
	else:
		get_access_token()

def get_access_token():

	url = 'https://api.codechef.com/oauth/token'

	data = {
		'client_id': client_id,
		'client_secret': client_secret,
		'refresh_token': cred_file.refresh_token,
		'grant_type': 'refresh_token'
	}

	response = requests.post(
		url=url,
		data=data,
	)
	response = response.json()
	generated_on = str(datetime.datetime.now())

	cred_file.access_token = response['result']['data']['access_token']
	cred_file.refresh_token = response['result']['data']['refresh_token']
	cred_file.generated_on = generated_on

	with open('credentials.py', "w+") as file:
		file.write("access_token = '"+response['result']['data']['access_token']+"'\n")
		file.write("refresh_token = '"+response['result']['data']['refresh_token']+"'\n")
		file.write("generated_on = '"+generated_on+"'")
	file.close()

	return True


def verify_login(auth_token):
	url = 'https://api.codechef.com/oauth/token'
	login_headers = {'content-Type': 'application/json',}
	data = '{{"grant_type": "authorization_code","code": "{}","client_id":"{}","client_secret":"{}","redirect_uri":"{}"}}'.format(auth_token, client_id, client_secret, redirect_uri)
	response = requests.post(url, headers=login_headers, data=data)
	response = response.json()

	print(response)
	if(response['status'] != 'OK'):
		return False
	else:
		access_token = response['result']['data']['access_token']
		refresh_token = response['result']['data']['refresh_token']
		generated_on = str(datetime.datetime.now())

		a = "access_token = '"+str(access_token)+"'\n"
		b = "refresh_token = '"+str(refresh_token)+"'\n"
		c = "generated_on = '"+str(generated_on)+"'\n"
		print(a, b, c )
		with open('credentials.py', "w+") as file:
			file.write(a)
			file.write(b)
			file.write(c)
		file.close()
		get_my_details()
		return True


def return_contest_details(contest_code):
	"""
	This function returns name, startdate, enddate of given contest
	using it's contest code.

	Input:
	A contest code in string datatype.

	Output:
	A json variable with values.
	"""
	activate_access_token()
	url = "https://api.codechef.com/contests/"+contest_code
	data = requests.get(url=url,headers=headers)
	data = data.json()
	problems = []
	for i in data['result']['data']['content']['problemsList']:
		problems.append(i['problemCode'])
	# print(problems)
	obj = {
		'name': data['result']['data']['content']['name'],
		'start_date': data['result']['data']['content']['startDate'],
		'end_date': data['result']['data']['content']['endDate'],
		'problems':problems
	}
	return obj


def return_problem_details(contest_code, problem_code):
	activate_access_token()
	url = "https://api.codechef.com/contests/"+contest_code+"/problems/"+problem_code
	# print(url)
	data = requests.get(url=url,headers=headers)
	data = data.json()
	print(data)
	obj = {
		'name': data['result']['data']['content']['problemName'],
		'timelimit': data['result']['data']['content']['maxTimeLimit'],
		'sizelimit': data['result']['data']['content']['sourceSizeLimit'],
		'body': data['result']['data']['content']['body'],
	}
	return obj



def test():
	url = 'https://api.codechef.com/submissions/?result=&year=&username=&language=&problemCode=&contestCode=&fields='
	a = requests.get(url = url , headers  = headers)
	parsed = a.json()
	# for val in parsed['result']['data']['content']:
	# 	print(val['result'] , val["date"] , val["problemCode"])
	# print(json.dumps(parsed, indent=4))	
	sub_list = []
	for val in parsed['result']['data']['content']:
		# if val['problemCode'] in problems:
			# v_contest_start_time = datetime.datetime.strptime(v_contest_start_time, fmt + ".%f")
			# end_time = v_contest_start_time + datetime.timedelta(minutes = int(float(duration)))
			# v_contest_start_time = time_slice(v_contest_start_time)
			# end_time = time_slice(end_time)
			# start_time = datetime.datetime.strptime(v_contest_start_time , fmt)
			# end_time = datetime.datetime.strptime(end_time , fmt)
			# sub_time = datetime.datetime.strptime(val['date'],fmt)
			# if sub_time>=start_time and sub_time<=end_time:
		lis = []
		for j in val:
			lis.append(val[j])
		sub_list.append(lis)
	print(sub_list)
	myFile = open('out1.csv', 'a')
	with myFile:
		writer = csv.writer(myFile)
		writer.writerows(sub_list)	


# test()
# activate_access_token()

def get_my_details():
	activate_access_token()
	url = "https://api.codechef.com/users/me"
	data = requests.get(url = url, headers = headers)
	data = data.json()
	username = data['result']['data']['content']['username']
	with open('user_details.py', 'w') as f:
		f.write("username = '"+username+"'\n")

# get_my_details()

# def test():
# 	url = 'https://api.codechef.com/ide/run'
# 	data = {
#   		"sourceCode": "#include <iostream>\n int main() { std::cout << \"Hi!\"; return 0; }",
#   		"language": "C++ 4.3.2",
#   		"input": "1 2 3"
# 	}
# 	a = requests.post(url = url , data  = data)
# 	parsed = a.json()
# 	print(json.dumps(parsed, indent=4))	

