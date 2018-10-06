import pymongo, os
import csv

# Set Password in Environment Variable named 'DB_PASSKEY' 
passw = os.environ['DB_PASSKEY']

# ADD URI STRING HERE #################################

# uri_string =  ""

#########################################################

client = pymongo.MongoClient(uri_string)

db = client.db