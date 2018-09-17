import csv
from collections import defaultdict
import operator
import json
from datetime import datetime
def diff(t1 , t2):
	fmt = '%Y-%m-%d %H:%M:%S'
	tstamp1 = datetime.strptime(t1, fmt)
	tstamp2 = datetime.strptime(t2, fmt)
	p = tstamp2 - tstamp1
	return p.total_seconds()
def convert(t):
	t = int(t)
	hour = t//3600
	t%=3600
	mint = t//60
	t%=60
	sec = t
	return str(hour)+":"+str(mint)+":"+str(sec)
def ranking(contest_code , problems_list , original_start_time , start_time , current_time):
	link = '../COOKOFF-dataset/' + contest_code + '.csv'
	with open(link) as csvfile:
		match = {}
		ranklist = []
		current_rank_list = []
		readcsv = list(csv.reader(csvfile , delimiter = ','))
		for row in readcsv:
			l = len(row)
			for j in range(0,l):
				if row[j] == "date":
					match["date"] = j
				if row[j] == "username":
					match["username"] = j
				if row[j] == "problemCode":
					match["problemCode"] = j
				if row[j] == "result":
					match["result"] = j
			break
		readcsv.reverse()
		total_names = set()
		for row in readcsv:
			if row[match["username"]] != "username":
				total_names.add(row[match["username"]])
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
		for row in readcsv:
			time_diff1 = diff(start_time , current_time)
			time_diff2 = diff(original_start_time , row[match["date"]])
			if time_diff2 > time_diff1:
				break
			username = row[match["username"]]
			for i in range(0,len(ranklist)):
				if ranklist[i]['name'] == username:
					ranklist[i]['entry'] = True
					if row[match["result"]] == "AC" and ranklist[i][row[match["problemCode"]]] <= 0:
						ranklist[i][row[match["problemCode"]]] = 1 + (ranklist[i][row[match["problemCode"]]] * (-1))
						ranklist[i][row[match["problemCode"]]+"Time"] = time_diff2

					elif ranklist[i][row[match["problemCode"]]]<=0:
						ranklist[i][row[match["problemCode"]]]-=1
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
		# print(current_rank_list)
		return current_rank_list

def dashboard(contest_code , problems_list, original_start_time , start_time , current_time):
	link = '../COOKOFF-dataset/' + contest_code + '.csv'
	with open(link) as csvfile:
		match = {}
		readcsv = list(csv.reader(csvfile , delimiter = ','))
		for row in readcsv:
			l = len(row)
			for j in range(0,l):
				if row[j] == "date":
					match["date"] = j
				if row[j] == "username":
					match["username"] = j
				if row[j] == "problemCode":
					match["problemCode"] = j
				if row[j] == "result":
					match["result"] = j
			break
		readcsv.reverse()
		submission = []
		for val in problems_list:
			p = {}
			p['problem_name'] = val
			p['correct'] = 0
			p['total'] = 0
			p['accuracy'] = 0
			submission.append(p)
		for row in readcsv:
			time_diff1 = diff(start_time , current_time)
			time_diff2 = diff(original_start_time , row[match["date"]])
			if time_diff2 > time_diff1:
				break
			for i in range(0,len(submission)):
				if submission[i]['problem_name'] == row[match["problemCode"]]:
					if row[match["result"]] == 'AC':
						submission[i]['correct']+=1
					submission[i]['total']+=1
					submission[i]['accuracy'] = str(round((submission[i]['correct']/submission[i]['total'])*100 , 2))
		# json_file = json.dumps(submission , indent = 4)
		# print(json_file)
		return submission
# ranking('COOK01' , problems , '2010-07-24 21:30:00' , '2018-09-17 16:40:00' , '2018-09-17 16:53:00')
# dashboard('2018-06-17 21:30:00' , '2018-06-17 21:45:00')