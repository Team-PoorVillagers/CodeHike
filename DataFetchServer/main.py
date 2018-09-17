import requests
import json
import pickle
import csv
import time 
import datetime
from credentials import *

headers = {
    'content-type': 'application/json',
    'Authorization': 'Bearer {}'.format(access_token)
}


def activate_access_token():
    if(generated_on != ""):
        # generated_on = generated_on.split(".")[0]
        fmt = '%Y-%m-%d %H:%M:%S.%f'
        tstamp1 = datetime.datetime.strptime(generated_on, fmt)
        tstamp2 = datetime.datetime.now()
        diff = tstamp2 - tstamp1
        # x = seconds since access token generated
        x = diff.total_seconds()
        # given access token expires in 3600 seconds, taking 3000 as limit 
        if(int(x) > 3300):
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

    if(response['status'] == 'error'):
        print("ERROR !! --- ", response['result']['errors']['message'])
        exit(0)
    generated_on = str(datetime.datetime.now())

    print(" access token updated ")
    with open('credentials.py', "w") as file:
        file.write("access_token = '"+response['result']['data']['access_token']+"'\n")
        file.write("refresh_token = '"+response['result']['data']['refresh_token']+"'\n")
        file.write("client_id = '"+client_id+"'\n")
        file.write("client_secret = '"+client_secret+"'\n")
        file.write("generated_on = '"+generated_on+"'")


# Writing script for LTime

contestCode = 1

adone = False

while(contestCode <= 63):

    if(contestCode < 10):
        cc = '0'+ str(contestCode)
        contestCode += 1
    elif(contestCode < 58):
        cc = contestCode
        contestCode += 1
    else:
        if(adone == False):
            cc = str(contestCode) + 'A'
            adone = True
        else:
            cc = str(contestCode) + 'B'
            adone = False
            contestCode += 1

    flag = 0     
    filename = 'LTIME'+ cc + '.csv'   
    myFile = open(filename, 'a')            
    cc = cc.upper()                                                               
    i = 1
    print("currently fetching ", cc)
    fetching_results = True

    while(fetching_results):
            # print(i)
            activate_access_token()
            print(cc)

            url = 'https://api.codechef.com/submissions/?contestCode='+str(cc)+'&offset='+str(i)+'&limit=100'
            i += 20
            a = requests.get(url=url,headers=headers)
            parsed = a.json()

            main_list = []
            heading = []

            #"message": "no submissions found for this search",
            print parsed
            if(parsed["result"]["data"]["code"] == 9003):
                print("results fetched for ", cc) 
                fetching_results = False
                break

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
                    writer = csv.writer(myFile)
                    writer.writerows(main_list)
            except:
                    break

            time.sleep(12)