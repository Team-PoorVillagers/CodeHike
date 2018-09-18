import requests
import json
import datetime
import csv

def time_slice(t):
    t = str(t)
    return t[:-7]

def activate_access_token():
	with open('credentials.json', 'r') as f:
		data = json.load(f)
		f.close()
	if(data['generated_on'] != ""):
		fmt = '%Y-%m-%d %H:%M:%S.%f'
		tstamp1 = datetime.datetime.strptime(data['generated_on'], fmt)
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

	with open('global_app_details.json', 'r') as f:
		app_data = json.load(f)
	f.close()

	with open('credentials.json', 'r') as f:
		client_data = json.load(f)
	f.close()

	url = 'https://api.codechef.com/oauth/token'

	data = {
		'client_id': app_data['client_id'],
		'client_secret': app_data['client_secret'],
		'refresh_token': client_data['refresh_token'],
		'grant_type': 'refresh_token'
	}

	response = requests.post(
		url=url,
		data=data,
	)
	response = response.json()
	generated_on = str(datetime.datetime.now())

	access_token = response['result']['data']['access_token']
	refresh_token = response['result']['data']['refresh_token']
	
	new_cred_data = {
			"access_token": str(access_token),
			"refresh_token": str(refresh_token),
			"generated_on":str(generated_on),
			}

	json_data = json.dumps(new_cred_data)
	f = open("credentials.json","w+")
	f.write(json_data)
	f.close()

	print("access token updated!!")
	return True


def verify_login(auth_token):

	with open('global_app_details.json', 'r') as f:
		app_data = json.load(f)
	f.close()

	url = 'https://api.codechef.com/oauth/token'
	login_headers = {'content-Type': 'application/json',}
	data = '{{"grant_type": "authorization_code","code": "{}","client_id":"{}","client_secret":"{}","redirect_uri":"{}"}}'.format(auth_token, app_data["client_id"], app_data["client_secret"], app_data["redirect_uri"])
	response = requests.post(url, headers=login_headers, data=data)
	response = response.json()

	if(response['status'] != 'OK'):
		return False
	else:
		access_token = response['result']['data']['access_token']
		refresh_token = response['result']['data']['refresh_token']
		generated_on = str(datetime.datetime.now())

		new_cred_data = {"access_token":access_token,"refresh_token":refresh_token,"generated_on":generated_on,}
		
		json_data = json.dumps(new_cred_data)
		f = open("credentials.json","w+")
		f.write(json_data)
		f.close()

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
	with open('credentials.json', 'r') as f:
		client_data = json.load(f)
	f.close()
	headers = {
	'content-type': 'application/json',
	'Authorization': 'Bearer {}'.format(client_data["access_token"])
	}
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

	with open('credentials.json', 'r') as f:
		client_data = json.load(f)
	f.close()
	headers = {
	'content-type': 'application/json',
	'Authorization': 'Bearer {}'.format(client_data["access_token"])
	}
	url = "https://api.codechef.com/contests/"+contest_code+"/problems/"+problem_code
	# print(url)
	data = requests.get(url=url,headers=headers)
	data = data.json()
	# print(data)
	obj = {
		'name': data['result']['data']['content']['problemName'],
		'timelimit': data['result']['data']['content']['maxTimeLimit'],
		'sizelimit': data['result']['data']['content']['sourceSizeLimit'],
		'body': data['result']['data']['content']['body'],
	}
	return obj



def test():

	with open('credentials.json', 'r') as f:
		client_data = json.load(f)
	f.close()
	headers = {	
	'content-type': 'application/json',
	'Authorization': 'Bearer {}'.format(client_data["access_token"])
	}

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
	# print(sub_list)
	myFile = open('out1.csv', 'a')
	with myFile:
		writer = csv.writer(myFile)
		writer.writerows(sub_list)	


def get_my_details():

	url = "https://api.codechef.com/users/me"	
	with open('credentials.json', 'r') as f:
		client_data = json.load(f)
	f.close()
	headers = {	
	'content-type': 'application/json',
	'Authorization': 'Bearer {}'.format(client_data["access_token"])
	}
	data = requests.get(url = url, headers = headers)
	data = data.json()
	username = data['result']['data']['content']['username']
	user_data = {"username":username}
	json_data = json.dumps(user_data)
	f = open("user_data.json","w+")
	f.write(json_data)
	f.close()




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

