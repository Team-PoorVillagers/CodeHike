import csv
from collections import defaultdict
import operator
import json
ranks = {}
ranklist = []
with open('out.csv') as csvfile:
	readcsv = list(csv.reader(csvfile , delimiter = ','))
	readcsv.reverse()
	total_names = set()
	total_problems = set()
	for row in readcsv:
		total_names.add(row[3])
		total_problems.add(row[4])
	# print(total_names)
	# print(total_problems)
	for name in total_names:
		user = {}
		user['name'] = name
		user['entry'] = False
		user['Total Score'] = 0
		for problem in total_problems:
			user[problem] = 0
		ranklist.append(user)
	for row in readcsv:
		username = row[3]
		for i in range(0,len(ranklist)):
			if ranklist[i]['name'] == username:
				ranklist[i]['entry'] = True
				penalty = 0
				score = 0
				if row[6] == "AC" and ranklist[i][row[4]] <= 0:
					ranklist[i][row[4]]+=100000000
				elif ranklist[i][row[4]]<=0:
					ranklist[i][row[4]]-=20
				ranklist[i]['Total Score'] = 0
				for problem in total_problems:
					if ranklist[i][problem] > 0:
						ranklist[i]['Total Score']+=ranklist[i][problem]
		ranklist.sort(key=operator.itemgetter('Total Score') , reverse = True)
	json_file = json.dumps(ranklist , indent = 4)
	print(json_file)
	# for i in range(len_csv , 1, -1):
	# 	print(readcsv['username'])