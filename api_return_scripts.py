import requests
import json
import datetime
import csv
import os
from db_conn import db

from flask import session

from db_conn import db


def time_slice(t):
	"""
	Removes Miliseconds from Python time stamp
	Ex - 11:07:23.1323232 --> 11:07:23
	Args : A time stamp
	Returns : Clean Time stamp
	"""	
    t = str(t)
    return t[:-7]


def diff(t1 , t2):
	p = t2 - t1
	return p.total_seconds()

def diff1(t1 , t2):
	"""
	Get time difference between two time stamp in seconds

	Args : Two time stamps

	Returns : Time Difference in seconds.
	""" 
	fmt = '%Y-%m-%d %H:%M:%S'
	tstamp1 = datetime.datetime.strptime(str(t1), fmt)
	tstamp2 = datetime.datetime.strptime(str(t2), fmt)
	p = tstamp2 - tstamp1
	return p.total_seconds()

def convert(t):
	"""
	Converts given no. of seconds to HH:MM:SS format

	Args : time in seconds

	Returns : String in HH:MM:SS format.
	"""
	t = int(t)
	hour = t//3600
	t%=3600
	mint = t//60
	t%=60
	sec = t
	return str(hour)+":"+str(mint)+":"+str(sec)

def activate_access_token():
	"""
	Checks whether the access token has expired or not, 
	If expired then calls get_access_token() 

	Args : None

	Returns : None
	"""
	username = session['username']
	user_data = db['user_data'].find_one({'_id':username})
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
	"""
	Updates Access Token and Refresh Token by making a API call.

	Args: None

	Returns : None 
	"""
	field = db['app_data'].find()
	app_data = field[0]

	username = session['username']
	user_data = db['user_data'].find_one({'_id':username})

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


def verify_login(auth_token):
	"""
	Verifies User Login, If true then stores Username, Access Token, refresh token in DB

	Args : Auth Token

	Returns : True when Successfull else False
	"""
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
		session_list = []
		# session_list = [{'problems' : list() , 'contest_start_time' : None , 'contest_end_time' : None , 'duration' : None , 'contest_code' : None , 'contest_name' : None , 'v_contest_start_time' : None}]
		access_token = response['result']['data']['access_token']
		refresh_token = response['result']['data']['refresh_token']
		generated_on = str(datetime.datetime.now())
		username = get_my_details(access_token)
		if(db['user_data'].find_one({'_id':username}) == None):
			db['user_data'].insert({'_id':username,'access_token':access_token,'refresh_token':refresh_token,
				'generated_on':generated_on , 'friends' : list() , 'problems' : list() , 'contest_start_time' : None , 'contest_end_time' : None , 'duration' : None , 'contest_code' : None , 'contest_name' : None , 'v_contest_start_time' : None , 'is_running' : False	,'submissions' : dict()})
		else:
			db['user_data'].update({'_id': username},{ '$set':{'access_token': access_token, 'refresh_token':refresh_token, 'generated_on':generated_on , 'problems' : list() , 'contest_start_time' : None , 'contest_end_time' : None , 'duration' : None , 'contest_code' : None , 'contest_name' : None , 'v_contest_start_time' : None , 'is_running' : False	,'submissions' : dict()}}, upsert=False)


		session['username'] = username
		return True


def return_contest_details(contest_code):
	"""
	This function returns name, startdate, enddate of given contest
	using it's contest code.

	Input :	A contest code in string datatype.

	Output : A json variable with values.
	"""
	username = session['username']
	user_data = db['user_data'].find_one({'_id':username})

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
	"""
	Get Problem Details such as Name, Time limit, Sizelimit, problem statement

	Args : Contest code and Problem Code

	Returns : A JSON object containing required value.

	"""
	activate_access_token()
	username = session['username']
	user_data = db['user_data'].find_one({'_id':username})

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
	"""
	Get Username of Logged-In User

	Args: Access Token
	
	Returns : Username
	"""
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
	"""
	Fetch Submission of LoggedIn User.
	This function is used to get submission data of user while virtual contest is running.
	It checks whether submission to problems in Virtual contest is done within the start-end time of virtual 
	contest.

	Args : None

	Returns : None
	"""
	fmt = '%Y-%m-%d %H:%M:%S'
	username = session['username']
	user_data = db['user_data'].find_one({'_id':username})
	v_contest_start_time = user_data['v_contest_start_time']
	contest_start_time = user_data['contest_start_time']
	duration = user_data['duration']
	is_running = user_data['is_running']
	contest_code = user_data['contest_code']
	contest_name = user_data['contest_name']
	problems = user_data['problems']
	submissions = user_data['submissions']
	headers = {	
	'content-type': 'application/json',
	'Authorization': 'Bearer {}'.format(user_data["access_token"])
	}

	url = 'https://api.codechef.com/submissions/?result=&year=&username=' + username + '&language=&problemCode=&contestCode=&fields='
	# print(url)
	data = requests.get(url = url , headers = headers)
	# print(data)	
	parsed = data.json()
	print(parsed)
	if parsed['result']['data']['code'] == 9001:
		
		for row in parsed['result']['data']['content']:
			if row['problemCode'] in problems:
				start_time = datetime.datetime.strptime(str(v_contest_start_time) , fmt + ".%f")
				end_time = start_time + datetime.timedelta(minutes = int(float(duration)))
				start_time = time_slice(start_time)
				end_time = time_slice(end_time)
				start_time = datetime.datetime.strptime(str(start_time) , fmt)
				end_time = datetime.datetime.strptime(str(end_time) , fmt)
				sub_time = datetime.datetime.strptime(str(row['date']),fmt)
				if sub_time>=start_time and sub_time<=end_time:
					# print(start_time , end_time , sub_time)
					if row['id'] not in submissions[row['problemCode']]:
						collections = db[contest_code]
						new_row  = {}
						time_diff = diff(start_time , sub_time)
						original_time = datetime.datetime.strptime(str(contest_start_time) , fmt)
						modify_time = original_time + datetime.timedelta(seconds = int(time_diff))
						for val in collections.find_one():
							if val!='_id':
								new_row[val] = row[val]
						new_row['date'] = str(modify_time)
						new_row['username'] = '*' + username
						collections.insert(new_row)
						submissions[row['problemCode']].append(row['id'])
						db['user_data'].update_one({'_id': username}, {'$set': {'submissions': submissions}})

def compare_results(compare_with, contestcode , curr_time):
	"""
	Compares progress of given user with logged in user on 
	parameter such as language, time, panelty

	Args : username_to_compare_with, contest code and curr time

	Returns : Dictionary contaning required values
	"""
	username = session['username']
	user_data = db['user_data'].find_one({'_id':username})
	v_contest_start_time = user_data['v_contest_start_time']
	contest_start_time = user_data['contest_start_time']
	duration = user_data['duration']
	is_running = user_data['is_running']
	contest_code = user_data['contest_code']
	contest_name = user_data['contest_name'] 
	problems = user_data['problems']
	from datetime import datetime

	fmt = '%Y-%m-%d %H:%M:%S'
	v_contest_start_time = time_slice(v_contest_start_time)
	curr_time = time_slice(curr_time)
	data_dict = dict()
	username2 = compare_with
	for i in problems:
		tries = 0
		kk = []
		x = db[contestcode].find({'username':'*'+username,'problemCode':str(i)}).sort('id')
		flag = False
		for k in x:
			time_diff1 = diff1(v_contest_start_time , curr_time)
			time_diff2 = diff1(contest_start_time , k['date'])
			if time_diff2 > time_diff1:
				break
			if(k['result'] == 'AC'):
				date = k['date']
				tstamp1 = datetime.strptime(str(contest_start_time), fmt)
				tstamp2 = datetime.strptime(str(date), fmt)
				td = tstamp2 - tstamp1
				td_mins = convert(td.total_seconds())
				oo = [td_mins, k['time'], k['language'], tries]
				kk.append(oo)
				flag = True
				break
			tries += 1
		if(flag == False):
			oo = [tries]
			kk.append(oo)
		tries = 0
		x = db[contestcode].find({'username':username2,'problemCode':str(i)}).sort('id')
		flag = False
		for k in x:
			time_diff1 = diff1(v_contest_start_time , curr_time)
			time_diff2 = diff1(contest_start_time , k['date'])
			if time_diff2 > time_diff1:
				break
			if(k['result'] == 'AC'):
				date = k['date']
				tstamp1 = datetime.strptime(str(contest_start_time), fmt)
				tstamp2 = datetime.strptime(str(date), fmt)
				td = tstamp2 - tstamp1
				td_mins = convert(td.total_seconds())
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