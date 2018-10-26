import pymongo, os
import csv

# ADD URI STRING HERE #################################
# set production False, if you want to contribute to this repo and make changes
production = False

uri_string =  ""


#########################################################
 
client = pymongo.MongoClient(uri_string)
 
db = client.db