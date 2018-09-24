import datetime
from flask import Flask, render_template, jsonify, request, redirect,  url_for, flash, session, abort
from ranklist_extraction import ranking,dashboard
from api_return_scripts import *
import json
import os
app = Flask(__name__)

@app.route("/")
def main_page():
    if not session.get('logged_in'):
        with open('global_app_details.json', 'r') as f:
            app_data = json.load(f)
            # print(app_data)
        f.close()
        return render_template("home-no-login.html", client_id = app_data["client_id"], redirect_uri = app_data["redirect_uri"])
    else:
        with open('user_data.json', 'r') as f:
            user_data = json.load(f)
        f.close()
        return render_template("home.html", username = user_data['username'], contest_code_display = False)


@app.route('/auth', methods=['GET'])
def do_login():
    auth_token = request.args.get("code")
    x = verify_login(auth_token)
    if (x == True):
        session['logged_in'] = True
        # get_my_details()
    else:
        flash('wrong password!')
    return main_page()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    os.remove('credentials.json')
    return main_page()

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")


@app.route("/friends")
def friends():
    return render_template("friends.html")


@app.route("/contestpage/<contest_code>")
def contest_page(contest_code):
    x = return_contest_details(contest_code)
    fmt = '%Y-%m-%d %H:%M:%S'
    s_d = datetime.datetime.strptime(x['start_date'], fmt)
    e_d = datetime.datetime.strptime(x['end_date'], fmt)
    diff = e_d - s_d
    diff = diff.total_seconds()/60

    from session import problems,v_contest_start_time,contest_start_time,duration

    time_now = time_slice(datetime.datetime.now())
    v_contest_start_time = datetime.datetime.strptime(v_contest_start_time, fmt + ".%f")
    end_time = v_contest_start_time + datetime.timedelta(minutes = int(float(duration)))
    v_contest_start_time = time_slice(v_contest_start_time)
    end_time = time_slice(end_time)
    tstamp1 = datetime.datetime.strptime(time_now , fmt)
    tstamp2 = datetime.datetime.strptime(end_time , fmt)
    p = tstamp2 - tstamp1
    p = p.total_seconds()
    fetch_submission()
    obj = dashboard(contest_code , problems  , contest_start_time , v_contest_start_time , time_now)
    with open('user_data.json', 'r') as f:
        user_data = json.load(f)
    f.close()
    return render_template("contestpage.html",contest_code = contest_code, name = x['name'], mins = diff, problems = x['problems'] , obj = obj , time = p, username = user_data['username'], contest_code_display = True)

@app.route("/standings")
def current_standing():

    from session import problems,v_contest_start_time,contest_start_time,duration,contest_code
    fmt = '%Y-%m-%d %H:%M:%S'
    v_contest_start_time = datetime.datetime.strptime(v_contest_start_time, fmt + ".%f")
    v_contest_start_time = time_slice(v_contest_start_time)
    now = time_slice(datetime.datetime.now())
    # print(v_contest_start_time , now)
    fetch_submission()
    obj = ranking(contest_code , problems , contest_start_time , v_contest_start_time , now)
    with open('user_data.json', 'r') as f:
        user_data = json.load(f)
    f.close()
    return render_template("rankings.html", obj=obj , problems = problems, username = user_data['username'], contest_code = contest_code, contest_code_display = True)

@app.route("/problem/<contest_code>/<problem_code>")
def problem_details(contest_code, problem_code):
    x = return_problem_details(contest_code, problem_code)
    with open('user_data.json', 'r') as f:
        user_data = json.load(f)
    f.close()
    return render_template('problem.html', name = x['name'], timelimit = x['timelimit'], \
        sizelimit = x['sizelimit'], statement = x['body'], username = user_data['username'], problem_code = problem_code ,contest_code = contest_code, contest_code_display = True)


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
    fmt = '%Y-%m-%d %H:%M:%S'
    s_d = datetime.datetime.strptime(obj['start_date'], fmt)
    e_d = datetime.datetime.strptime(obj['end_date'], fmt)
    duration = e_d - s_d
    duration = duration.total_seconds()/60

    submissions = {}

    with open('session.py', "w") as file:
        file.write("problems = [ ")
        for i in obj['problems']:
            submissions[i] = []
            file.write("'"+i+"'")
            file.write(" , ")
        file.write(" ] \n")
        file.write("contest_start_time = '"+str(s_d)+"'\n")
        file.write("contest_end_time = '"+str(e_d)+"'\n")
        file.write("duration = '"+str(duration)+"'\n")
        file.write("contest_code = '"+str(contest_code)+"'\n")
    file.close()

    json_data = json.dumps(submissions)
    with open('submissions.json' , "w+") as f:
        f.write(json_data)

    with open('user_data.json', 'r') as f:
        user_data = json.load(f)
    f.close()

    return render_template("contest_welcome.html" ,contest_code = contest_code,\
     name = obj['name'], mins = duration, s_d = s_d, e_d = e_d , username = user_data['username'],contest_code_display = False )

@app.route("/begin_contest", methods=['POST'])
def begin_contest():
    contest_code = request.form['contestcode']
    v_contest_start_time = str(datetime.datetime.now())
    
    with open('session.py', "a") as file:
        file.write("v_contest_start_time = '"+v_contest_start_time+"'\n")

    with open('user_data.json', 'r') as f:
        user_data = json.load(f)
    f.close()

    return redirect(url_for('contest_page',contest_code = contest_code, username = user_data['username'], contest_code_display = True))


if __name__ == "__main__":
    app.secret_key = "this is super secret wanna lubba dub dub"
    app.run(debug=True)
