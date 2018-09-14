import requests
import json
import datetime

from credentials import access_token, refresh_token, client_id, client_secret, generated_on

headers = {
	'content-type': 'application/json',
	'Authorization': 'Bearer {}'.format(access_token)
}

def activate_access_token():
	if(generated_on != ""):
		fmt = '%Y-%m-%d %H:%M:%S.%f'
		tstamp1 = datetime.datetime.strptime(generated_on, fmt)
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
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }

    response = requests.post(
        url=url,
        data=data,
    )
    response = response.json()
    generated_on = str(datetime.datetime.now())

    with open('credentials.py', "w") as file:
    	file.write("access_token = '"+response['result']['data']['access_token']+"'\n")
    	file.write("refresh_token = '"+response['result']['data']['refresh_token']+"'\n")
    	file.write("client_id = '"+client_id+"'\n")
    	file.write("client_secret = '"+client_secret+"'\n")
    	file.write("generated_on = '"+generated_on+"'")

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