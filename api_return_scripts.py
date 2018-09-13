import requests
import json
from current_access_refresh_token import access_token, refresh_token

client_id = 'ef7441a4b097e998305fb63fe07ae8d1'
client_secret = 'd90fe771ec547a6f0d5c9e75962969e6'

headers = {
	'content-type': 'application/json',
	'Authorization': 'Bearer {}'.format(access_token)
}

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
    print(response)

    with open('current_access_refresh_token.py', "w") as file:
    	file.write("access_token = '"+response['result']['data']['access_token']+"'\n")
    	file.write("refresh_token = '"+response['result']['data']['refresh_token']+"'")
    # print (response.json())	

    return 1

print(get_access_token(client_id, client_secret, refresh_token))

def return_contest_details(contest_code):
	"""
	This function returns name, startdate, enddate of given contest
	using it's contest code.

	Input:
	A contest code in string datatype.

	Output:
	A json variable with values.
	"""
	url = "https://api.codechef.com/contests/"+contest_code
	data = requests.get(url=url,headers=headers)
	data = data.json()
	obj = {
		'name': data['result']['data']['content']['name'],
		'start_date': data['result']['data']['content']['startDate'],
		'end_date': data['result']['data']['content']['endDate']
	}
	return obj