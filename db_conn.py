import pymongo, os
import csv

passw = os.environ['DB_PASSKEY']

#passw = os.environ['DB_PASSKEY']
# ADD URI STRING HERE #################################

# uri_string =  ""


#########################################################

client = pymongo.MongoClient(uri_string)

db = client.db

# for code in range(28,92):
# 	contest_code = "COOK" + str(code)
# 	if contest_code not in db.collection_names():
# 		db.create_collection(contest_code)
# 	collection = db[contest_code]
# 	link = str(os.getcwd())+'/COOKOFF-dataset/' + contest_code + '.csv'
# 	flag = 0
# 	heading = []
# 	new_row = {}
# 	with open(link) as csvfile:
# 		readCSV = csv.reader(csvfile, delimiter=',')
# 		for row in readCSV:
# 			if not flag:
# 				heading = row
# 				flag = 1
# 			else:
# 				for j in range(0, len(row)):	
# 					new_row[heading[j]] = row[j]
# 				collections.insert(new_row) 
		
# collections = db['user_data']

# collections.delete_one({'_id' : 'hasan_356'})

# collections = db['COOK01']



# for collection in collections.find():
	# print(collection)
# print(collection.find_one())

# print(db)

# Example for you to do things. 

# Create a new collection
# db.create_collection("app_data")

# Get name of all collections 
# collects = db.collection_names(include_system_collections=False)

# Access Collections and update 
# collection = db['COOK01']
# collection.insert({'username':'hasan', 'score':600})
# collection.update_one({'_id': 1}, {'$set': {'x': 10}})
# To remove a collection
# db.drop_collection("COOK01")


# This is best resource for referance above commands and other as well :
# https://api.mongodb.com/python/current/api/pymongo/collection.html


"""
The DB follows following structure - 

Collections-
	- COOK01
	- COOK02

"""

# x = db['app_data'].find()

# print(x[0]['client_id'])
