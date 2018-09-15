import datetime

from flask import Flask, render_template, jsonify, request, redirect,  url_for

from ranklist_extraction import ranking,dashboard

from api_return_scripts import *


app = Flask(__name__)

def time_slice(t):
    t = str(t)
    return t[:-7]

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

    from session import problems,v_contest_start_time,contest_start_time,duration

    time_now = time_slice(datetime.datetime.now())
    # print("\n\n\n\n\n")
    # print(time_now , v_contest_start_time)
    v_contest_start_time = datetime.datetime.strptime(v_contest_start_time, fmt + ".%f")
    end_time = v_contest_start_time + datetime.timedelta(minutes = int(float(duration)))
    print(end_time)
    # print(str(datetime.timedelta(minutes = 10)))
    v_contest_start_time = time_slice(v_contest_start_time)
    end_time = str(end_time)
    end_time = end_time.split(".")[0]
    print(time_now , end_time)
    tstamp1 = datetime.datetime.strptime(time_now , fmt)
    tstamp2 = datetime.datetime.strptime(end_time , fmt)
    p = tstamp2 - tstamp1
    p = p.total_seconds()

    obj = dashboard(problems  , contest_start_time , v_contest_start_time , time_now)

    return render_template("contestpage.html",contest_code = contest_code, name = x['name'], mins = diff, problems = x['problems'] , obj = obj , time = p)

@app.route("/standings")
def current_standing():
    from session import problems,v_contest_start_time,contest_start_time,duration
    fmt = '%Y-%m-%d %H:%M:%S'
    v_contest_start_time = datetime.datetime.strptime(v_contest_start_time, fmt + ".%f")
    v_contest_start_time = time_slice(v_contest_start_time)
    now = time_slice(datetime.datetime.now())
    print(v_contest_start_time , now)
    obj = ranking(problems , contest_start_time , v_contest_start_time , now)
    # print(obj)
    return render_template("rankings.html", obj=obj , problems = problems)

@app.route("/problem/<contest_code>/<problem_code>")
def problem_details(contest_code, problem_code):
    print(contest_code, problem_code)
    # return render_template("home.html")

    print("api called ")
    x = return_problem_details(contest_code, problem_code)
    print(x)
    return render_template('problem.html', name = x['name'], timelimit = x['timelimit'], \
        sizelimit = x['sizelimit'], statement = x['body'])


# @app.route("/clock")
# def timer():
#     from session import problems,v_contest_start_time,contest_start_time,duration
#     time_now = time_slice(datetime.now())
#     end_time = v_contest_start_time + datetime.timedelta(minutes = int(duration))
#     end_time = time_slice(end_time)
#     fmt = '%Y-%m-%d %H:%M:%S'
#     tstamp1 = datetime.strptime(time_now , fmt)
#     tstamp2 = datetime.strptime(end_time, fmt)
#     print(tstamp1 , tstamp2)
#     p = tstamp2 - tstamp1
#     p = p.total_seconds()
#     return render_template("timer.html" , time = p)

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

    with open('session.py', "w") as file:
        file.write("problems = [ ")
        for i in obj['problems']:
            file.write("'"+i+"'")
            file.write(" , ")
        file.write(" ] \n")
        file.write("contest_start_time = '"+str(s_d)+"'\n")
        file.write("contest_end_time = '"+str(e_d)+"'\n")
        file.write("duration = '"+str(duration)+"'\n")
    file.close()
    return render_template("contest_welcome.html" ,contest_code = contest_code,\
     name = obj['name'], mins = duration, s_d = s_d, e_d = e_d  )

@app.route("/begin_contest", methods=['POST'])
def begin_contest():
    contest_code = request.form['contestcode']
    v_contest_start_time = str(datetime.datetime.now())
    
    with open('session.py', "a") as file:
        file.write("contest_code = '"+contest_code+"'\n")
        file.write("v_contest_start_time = '"+v_contest_start_time+"'\n")


    return redirect(url_for('contest_page',contest_code = contest_code))



if __name__ == "__main__":
	app.run(debug=True)