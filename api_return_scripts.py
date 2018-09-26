import requests
import json
import datetime
import csv
import os
from db_conn import db

from flask import session

from db_conn import db


def time_slice(t):
    t = str(t)
    return t[:-7]


def diff(t1 , t2):
	p = t2 - t1
	return p.total_seconds()

def activate_access_token():
	username = session['username']
	user_data = db['user_data'].find({'_id':username})
	user_data = user_data[0]

	if(user_data['generated_on'] != ""):
		fmt = '%Y-%m-%d %H:%M:%S.%f'
		tstamp1 = datetime.datetime.strptime(user_data['generated_on'], fmt)
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

	field = db['app_data'].find()
	app_data = field[0]

	username = session['username']
	user_data = db['user_data'].find({'_id':username})
	user_data = user_data[0]

	url = 'https://api.codechef.com/oauth/token'

	data = {
		'client_id': app_data['client_id'],
		'client_secret': app_data['client_secret'],
		'refresh_token': user_data['refresh_token'],
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

	db['user_data'].update({'_id': username},{ '$set':{'access_token': access_token, 'refresh_token':refresh_token, 'generated_on':generated_on}}, upsert=False)

	print("access token updated!!")
	return True


def verify_login(auth_token):

	field = db['app_data'].find()
	app_data = field[0]

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
		username = get_my_details(access_token)
		if(db['user_data'].find_one({'_id':username}) == None):
			db['user_data'].insert({'_id':username,'access_token':access_token,'refresh_token':refresh_token,
				'generated_on':generated_on , 'friends' : list()})
		else:
			db['user_data'].update({'_id': username},{ '$set':{'access_token': access_token, 'refresh_token':refresh_token, 'generated_on':generated_on}}, upsert=False)


		session['username'] = username
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
	username = session['username']
	user_data = db['user_data'].find({'_id':username})
	user_data = user_data[0]

	headers = {
	'content-type': 'application/json',
	'Authorization': 'Bearer {}'.format(user_data["access_token"])
	}
	activate_access_token()
	url = "https://api.codechef.com/contests/"+contest_code
	data = requests.get(url=url,headers=headers)
	data = data.json()
	# print(data)
	problems = []
	# print(data)
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

	username = session['username']
	user_data = db['user_data'].find({'_id':username})
	user_data = user_data[0]

	headers = {
	'content-type': 'application/json',
	'Authorization': 'Bearer {}'.format(user_data["access_token"])
	}
	url = "https://api.codechef.com/contests/"+contest_code+"/problems/"+problem_code
	data = requests.get(url=url,headers=headers)
	data = data.json()
	obj = {
		'name': data['result']['data']['content']['problemName'],
		'timelimit': data['result']['data']['content']['maxTimeLimit'],
		'sizelimit': data['result']['data']['content']['sourceSizeLimit'],
		'body': data['result']['data']['content']['body'],
	}
	return obj


def get_my_details(access_token):

	url = "https://api.codechef.com/users/me"	
	headers = {	
	'content-type': 'application/json',
	'Authorization': 'Bearer {}'.format(access_token)
	}
	data = requests.get(url = url, headers = headers)
	data = data.json()
	username = data['result']['data']['content']['username']
	return username


def fetch_submission():
	fmt = '%Y-%m-%d %H:%M:%S'
	from session import problems , contest_start_time , contest_end_time ,v_contest_start_time,duration,contest_code

	username = session['username']
	user_data = db['user_data'].find({'_id':username})
	user_data = user_data[0]

	headers = {	
	'content-type': 'application/json',
	'Authorization': 'Bearer {}'.format(user_data["access_token"])
	}

	url = 'https://api.codechef.com/submissions/?result=&year=&username=' + username + '&language=&problemCode=&contestCode=&fields='
	# print(url)
	data = requests.get(url = url , headers = headers)
	# print(data)	
	parsed = data.json()
	# print(parsed)
	if parsed['result']['data']['code'] == 9001:
		with open("submissions.json" , 'r') as f:
			submissions = json.load(f)
			for row in parsed['result']['data']['content']:
				if row['problemCode'] in problems:
					start_time = datetime.datetime.strptime(v_contest_start_time, fmt + ".%f")
					end_time = start_time + datetime.timedelta(minutes = int(float(duration)))
					start_time = time_slice(start_time)
					end_time = time_slice(end_time)
					start_time = datetime.datetime.strptime(start_time , fmt)
					end_time = datetime.datetime.strptime(end_time , fmt)
					sub_time = datetime.datetime.strptime(row['date'],fmt)
					if sub_time>=start_time and sub_time<=end_time:
						# print(start_time , end_time , sub_time)
						if row['id'] not in submissions[row['problemCode']]:
							collections = db[contest_code]
							ind = 0
							for row1 in collections.find():
								rank_time = datetime.datetime.strptime(row1['date'] , fmt)
								original_time = datetime.datetime.strptime(contest_start_time , fmt)
								time_diff1 = diff(start_time , sub_time)
								time_diff2 = diff(original_time , rank_time)
								if time_diff1 > time_diff2:
									ind = row1["id"]
									break
							# print(ind)
							new_row  = {}
							time_diff = diff(start_time , sub_time)
							original_time = datetime.datetime.strptime(contest_start_time , fmt)
							modify_time = original_time + datetime.timedelta(seconds = int(time_diff))
							for val in collections.find_one():
								if val!='_id':
									new_row[val] = row[val]
							new_row['date'] = str(modify_time)
							new_row['username'] = '*' + username
							collections.insert(new_row)
							submissions[row['problemCode']].append(row['id'])
							json_data = json.dumps(submissions)
							with open('submissions.json' , "w+") as f1:
								f1.write(json_data)
							f1.close()
		f.close()	


def compare_results(compare_with, contestcode):

	username = session['username']

	from session import problems, contest_start_time
	from datetime import datetime

	# username = 'saar_007'
	username2 = compare_with

	fmt = '%Y-%m-%d %H:%M:%S'

	data_dict = dict()

	for i in problems:
		tries = 0
		kk = []
		x = db[contestcode].find({'username':username, 'problemCode':str(i)})
		flag = False
		for k in x:
			if(k['result'] == 'AC'):
				date = k['date']
				tstamp1 = datetime.strptime(contest_start_time, fmt)
				tstamp2 = datetime.strptime(date, fmt)
				td = tstamp2 - tstamp1
				td_mins = int(round(td.total_seconds() / 60))
				oo = [td_mins, k['time'], k['language'], tries]
				kk.append(oo)
				flag = True
				break
			tries += 1
		if(flag == False):
			oo = [tries]
			kk.append(oo)
		tries = 0
		x = db[contestcode].find({'username':username2, 'problemCode':str(i)})
		flag = False
		for k in x:
			if(k['result'] == 'AC'):
				date = k['date']
				tstamp1 = datetime.strptime(contest_start_time, fmt)
				tstamp2 = datetime.strptime(date, fmt)
				td = tstamp2 - tstamp1
				td_mins = int(round(td.total_seconds() / 60))
				oo = [td_mins, k['time'], k['language'], tries]
				kk.append(oo)
				flag = True
				break
			tries += 1
		if(flag == False):
			oo = [tries]
			kk.append(oo)
		data_dict[i] = kk
		kk = []

	return data_dict

# fetch_submission()
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
