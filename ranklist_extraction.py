import csv
from collections import defaultdict
import operator
import json
from datetime import datetime

def convert(t):
	t = int(t)
	hour = t//3600
	t%=3600
	mint = t//60
	t%=60
	sec = t
	return str(hour)+":"+str(mint)+":"+str(sec)
def ranking(start_time , current_time):
	with open('out.csv') as csvfile:
		ranks = {}
		ranklist = []
		current_rank_list = []
		readcsv = list(csv.reader(csvfile , delimiter = ','))
		readcsv.reverse()
		total_names = set()
		problems_list = set()
		for row in readcsv:
			if row[0]!="id":
				total_names.add(row[3])
				problems_list.add(row[4])
		print(total_names)
		print(problems_list)
		for name in total_names:
			user = {}
			user['name'] = name
			user['entry'] = False
			user['Total Score'] = 0
			user['Penalty'] = 0
			user['Total'] = 0
			for problem in problems_list:
				user[problem] = 0
				user[problem+"Time"] = 0
			ranklist.append(user)
		# print(ranklist)
		for row in readcsv:
			fmt = '%Y-%m-%d %H:%M:%S'
			tstamp1 = datetime.strptime(start_time, fmt)
			tstamp2 = datetime.strptime(row[1], fmt)
			p = tstamp2 - tstamp1
			p = p.total_seconds()
			tstamp1 = datetime.strptime(current_time, fmt)
			tstamp2 = datetime.strptime(row[1], fmt)
			if tstamp2 > tstamp1:
				break
			username = row[3]
			for i in range(0,len(ranklist)):
				if ranklist[i]['name'] == username:
					ranklist[i]['entry'] = True
					if row[6] == "AC" and ranklist[i][row[4]] <= 0:
						ranklist[i][row[4]] = 1 + (ranklist[i][row[4]] * (-1))
						ranklist[i][row[4]+"Time"] = p

					elif ranklist[i][row[4]]<=0:
						ranklist[i][row[4]]-=1
					ranklist[i]['Total Score'] = 0
					ranklist[i]['Penalty'] = 0
					ranklist[i]['Total'] = 0
					for problem in problems_list:
						if ranklist[i][problem] > 0:
							ranklist[i]['Total Score']+=1
							ranklist[i]['Penalty']+=ranklist[i][problem+"Time"]
							ranklist[i]['Penalty']+=(ranklist[i][problem]-1)*600
							ranklist[i]['Total']+=100000000									
					ranklist[i]['Total']-=ranklist[i]['Penalty']
					ranklist[i]['Penalty'] = convert(ranklist[i]['Penalty'])
					break
		ranklist.sort(key=operator.itemgetter('Total') , reverse = True)
		for val in ranklist:
			if val['entry'] == True:
				current_rank_list.append(val)
		for val in current_rank_list:
			for problem in problems_list:
				val[problem+"Time"] = convert(val[problem+"Time"])
		json_file = json.dumps(current_rank_list , indent = 4)
		print(json_file)
		# for i in range(len_csv , 1, -1):
		# 	print(readcsv['username'])

ranking('2018-06-17 21:30:00' , '2018-06-17 23:59:00')