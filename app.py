import datetime

from flask import Flask, render_template, jsonify, request, redirect,  url_for

from ranklist_extraction import ranking,dashboard

from api_return_scripts import *

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template("home.html")

@app.route("/contestpage/<contest_code>")
def contest_page(contest_code):
    x = return_contest_details(contest_code)
    # print(x)
    # x = {'name': 'January Cook-Off 2018', 'start_date': '2018-01-21 21:30:00', 'end_date': '2018-01-22 00:00:00', 'problems': ['FINDA', 'MAGA', 'MULTHREE', 'FARGRAPH', 'SURVIVE']}
    fmt = '%Y-%m-%d %H:%M:%S'
    s_d = datetime.datetime.strptime(x['start_date'], fmt)
    e_d = datetime.datetime.strptime(x['end_date'], fmt)
    diff = e_d - s_d
    diff = diff.total_seconds()/60

    time_now = str(datetime.datetime.now())
    time_now = time_now[:-7]
    fmt = '%Y-%m-%d %H:%M:%S'
    tstamp1 = datetime.datetime.strptime(time_now , fmt)
    tstamp2 = datetime.datetime.strptime('2018-09-15 03:20:00', fmt)
    p = tstamp2 - tstamp1
    p = p.total_seconds()

    obj = dashboard('2018-06-17 21:30:00' , '2018-06-17 23:59:50')

    return render_template("contestpage.html",contest_code = contest_code, name = x['name'], mins = diff, problems = x['problems'] , obj = obj , time = p)

@app.route("/standings")
def current_standing():
    obj = ranking('2018-06-17 21:30:00' , '2018-06-17 22:59:00')
    print(obj)
    return render_template("rankings.html", obj=obj)

@app.route("/problem/<contest_code>/<problem_code>")
def problem_details(contest_code, problem_code):
    print(contest_code, problem_code)
    # return render_template("home.html")

    print("api called ")
    x = return_problem_details(contest_code, problem_code)
    print(x)
    return render_template('problem.html', name = x['name'], timelimit = x['timelimit'], \
        sizelimit = x['sizelimit'], statement = x['body'])


@app.route("/clock")
def timer():
    time_now = str(datetime.now())
    time_now = time_now[:-7]
    fmt = '%Y-%m-%d %H:%M:%S'
    tstamp1 = datetime.strptime(time_now , fmt)
    tstamp2 = datetime.strptime('2018-09-15 00:00:00', fmt)
    p = tstamp2 - tstamp1
    p = p.total_seconds()
    return render_template("timer.html" , time = p)

@app.route("/contest_welcome", methods=['GET'])
def welcome_page():
    contest_code = request.args.get("contestcode")
    contest_code.upper()

    obj = return_contest_details(contest_code)
    # obj = {'name': 'June Cook-Off 2018 Division 1', 'start_date': '2018-06-17 21:30:00', 'end_date': '2018-06-18 00:00:00', 'problems': ['SONYASEG', 'DANYANUM', 'MINIONS', 'BTMNTREE', 'NUMCOMP', 'GOODPERM']}

    fmt = '%Y-%m-%d %H:%M:%S'
    s_d = datetime.datetime.strptime(obj['start_date'], fmt)
    e_d = datetime.datetime.strptime(obj['end_date'], fmt)
    duration = e_d - s_d
    duration = duration.total_seconds()/60

    return render_template("contest_welcome.html" ,contest_code = contest_code,\
     name = obj['name'], mins = duration, s_d = s_d, e_d = e_d )

@app.route("/begin_contest", methods=['POST'])
def begin_contest():
    contest_code = request.form['contestcode']
    v_contest_start_time = request.form['time']
    contest_start_time = request.form['old_s_time']
    contest_end_time = request.form['old_e_time']
    duration = request.form['duration']
    
    with open('session.py', "w") as file:
        file.write("contest_code = '"+contest_code+"'\n")
        file.write("v_contest_start_time = '"+v_contest_start_time+"'\n")
        file.write("contest_start_time = '"+contest_start_time+"'\n")
        file.write("contest_end_time = '"+contest_end_time+"'\n")
        file.write("duration = '"+duration+"'")

    return redirect(url_for('contest_page',contest_code = contest_code))



if __name__ == "__main__":
	app.run(debug=True)