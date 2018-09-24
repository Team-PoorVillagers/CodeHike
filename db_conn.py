import pymongo, os

passw = os.environ['DB_PASSKEY']

uri_string =  "mongodb://root:"+str(passw)+"@dds-6gj13ff1b21a36b41209-pub.mongodb.ap-south-1.rds.aliyuncs.com:3717,dds-6gj13ff1b21a36b42533-pub.mongodb.ap-south-1.rds.aliyuncs.com:3717/admin?replicaSet=mgset-1050001983"

print(uri_string)

client = pymongo.MongoClient(uri_string)

db = client.db

print(db)
# Example for you to do things. 

# Create a new collection
# db.create_collection("COOK01")

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