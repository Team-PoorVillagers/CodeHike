import datetime
from flask import Flask, render_template, jsonify, request, redirect,  url_for, flash, session, abort
from ranklist_extraction import ranking,dashboard
from api_return_scripts import *
import json
import os
app = Flask(__name__)


@app.route("/")
def main_page():
    username = session['username']
    user_data = db['user_data'].find({'_id':username})
    user_data = user_data[0]
    v_contest_start_time = user_data['v_contest_start_time']
    contest_start_time = user_data['contest_start_time']
    duration = user_data['duration']
    is_running = user_data['is_running']
    contest_code = user_data['contest_code']
    contest_name = user_data['contest_name']
    if not session.get('logged_in'):
        field = db['app_data'].find()
        app_data = field[0]
        return render_template("home-no-login.html", client_id = app_data["client_id"], redirect_uri = app_data["redirect_uri"])
    else :
        if(is_running == False):
            return render_template("home.html", username = username, contest_code_display = False)
        else:
            return redirect(url_for('contest_page',contest_code = contest_code))


@app.route('/auth', methods=['GET'])
def do_login():
    auth_token = request.args.get("code")
    x = verify_login(auth_token)
    if (x == True):
        session['logged_in'] = True
        # get_my_details()
    else:
        pass
        # flash('wrong password!')
    return main_page()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return main_page()

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")


@app.route("/friends")
def friends():
    display_contest_code = True
    username = session['username']
    user_data = db['user_data'].find({'_id':username})
    user_data = user_data[0]
    contest_code = user_data['contest_code']
    if contest_code:
        #DO nothing
        display_contest_code = True
    else:
        display_contest_code = False
        contest_code = False

    username = session['username']
    friends_data = db['user_data'].find_one({'_id':username})
    friends = friends_data['friends']
    for i in range(0 ,len(friends)):
        friends[i].insert(0 , i+1)
    return render_template("friends.html", friends = friends , username = username , contest_code_display = display_contest_code , contest_code = contest_code)


@app.route("/contestpage/<contest_code>")
def contest_page(contest_code):
    username = session['username']
    user_data = db['user_data'].find({'_id':username})
    user_data = user_data[0]
    v_contest_start_time = user_data['v_contest_start_time']
    contest_start_time = user_data['contest_start_time']
    duration = user_data['duration']
    is_running = user_data['is_running']
    contest_code = user_data['contest_code']
    contest_name = user_data['contest_name']
    problems = user_data['problems']
    if(is_running == False):
            username = session['username']
            return render_template("home.html", username = username, contest_code_display = False)
    fmt = '%Y-%m-%d %H:%M:%S'
    time_now = time_slice(datetime.datetime.now())
    v_contest_start_time = datetime.datetime.strptime(str(v_contest_start_time), fmt + ".%f")
    end_time = v_contest_start_time + datetime.timedelta(minutes = int(float(duration)))
    v_contest_start_time = time_slice(v_contest_start_time)
    end_time = time_slice(end_time)
    tstamp1 = datetime.datetime.strptime(str(time_now) , fmt)
    tstamp2 = datetime.datetime.strptime(str(end_time) , fmt)
    p = tstamp2 - tstamp1
    p = p.total_seconds()
    fetch_submission()
    obj = dashboard(contest_code , problems  , contest_start_time , v_contest_start_time , time_now)
    return render_template("contestpage.html",contest_code = contest_code, name = contest_name, mins = duration, problems = problems , obj = obj , time = p, username = username, contest_code_display = True)

@app.route("/standings", methods=['GET'])
def current_standing():
    username = session['username']
    user_data = db['user_data'].find({'_id':username})
    user_data = user_data[0]
    v_contest_start_time = user_data['v_contest_start_time']
    contest_start_time = user_data['contest_start_time']
    duration = user_data['duration']
    is_running = user_data['is_running']
    contest_code = user_data['contest_code']
    contest_name = user_data['contest_name']
    problems = user_data['problems']
    if(is_running == False):
            username = session['username']
            return render_template("home.html", username = username, contest_code_display = False)
    friends = request.args.get("friends")

    # if friends == True, then user wants friends ranklist, each case you need
    # send a variable named friends, whose value can be True and False
    # if friends variable is True, that means data you sent is of friends.
    # there might be confusion as both GET variable and varible which we are sending 
    # both are named as friends.
    fmt = '%Y-%m-%d %H:%M:%S'
    v_contest_start_time = datetime.datetime.strptime(v_contest_start_time, fmt + ".%f")
    v_contest_start_time = time_slice(v_contest_start_time)
    now = time_slice(datetime.datetime.now())
    # print(v_contest_start_time , now)
    fetch_submission()
    obj = ranking(contest_code , problems , contest_start_time , v_contest_start_time , now , friends)
    username = session['username']
    user = {}
    user['rank'] = 0
    user['name'] = '*' + username
    user['entry'] = False
    user['Total Score'] = 0
    user['Penalty'] = 0
    user['Total'] = 0
    for problem in problems:
        user[problem] = 0
        user[problem+"Time"] = 0
    friend = user
    for val in obj:
        if val['name'] == '*' + username:
            friend = val
            break            
    return render_template("rankings.html", obj=obj , problems = problems, username = username, contest_code = contest_code, contest_code_display = True , friends = friends , friend = friend)

@app.route("/problem/<contest_code>/<problem_code>")
def problem_details(contest_code, problem_code):
    username = session['username']
    user_data = db['user_data'].find({'_id':username})
    user_data = user_data[0]
    v_contest_start_time = user_data['v_contest_start_time']
    contest_start_time = user_data['contest_start_time']
    duration = user_data['duration']
    is_running = user_data['is_running']
    contest_code = user_data['contest_code']
    contest_name = user_data['contest_name']
    problems = user_data['problems']
    if(is_running == False):
            username = session['username']
            return render_template("home.html", username = username, contest_code_display = False)
    x = return_problem_details(contest_code, problem_code)
    return render_template('problem.html', name = x['name'], timelimit = x['timelimit'], \
        sizelimit = x['sizelimit'], statement = x['body'], username = username, problem_code = problem_code ,contest_code = contest_code, contest_code_display = True)


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
    
    username = session['username']
    contest_code = request.args.get("contestcode")
    contest_code = contest_code.upper()

    obj = return_contest_details(contest_code)
    fmt = '%Y-%m-%d %H:%M:%S'
    s_d = datetime.datetime.strptime(obj['start_date'], fmt)
    e_d = datetime.datetime.strptime(obj['end_date'], fmt)
    duration = e_d - s_d
    contest_name = obj['name']
    duration = duration.total_seconds()/60

    submissions = {}
    for i in obj['problems']:
        submissions[i] = []

    db['user_data'].update_one({'_id': username}, {'$set': {'problems' : obj['problems'] , 'contest_start_time' : s_d , 'contest_end_time' : e_d , 'duration' : duration , 'contest_code' : contest_code , 'contest_name' : contest_name , 'submissions' : submissions}})

    # with open('session.py', "w+") as file:
    #     file.write("problems = [ ")
    #     for i in obj['problems']:
    #         submissions[i] = []
    #         file.write("'"+i+"'")
    #         file.write(" , ")
    #     file.write(" ] \n")
    #     file.write("contest_start_time = '"+str(s_d)+"'\n")
    #     file.write("contest_end_time = '"+str(e_d)+"'\n")
    #     file.write("duration = '"+str(duration)+"'\n")
    #     file.write("contest_code = '"+str(contest_code)+"'\n")
    #     file.write("contest_name = '"+str(contest_name)+"'\n")
    # file.close()


    return render_template("contest_welcome.html" ,contest_code = contest_code,\
     name = obj['name'], mins = duration, s_d = s_d, e_d = e_d , username = username ,contest_code_display = False )

@app.route("/begin_contest", methods=['POST'])
def begin_contest():
    contest_code = request.form['contestcode']
    v_contest_start_time = str(datetime.datetime.now())
    
    # with open('session.py', "a") as file:
    #     file.write("v_contest_start_time = '"+v_contest_start_time+"'\n")

    username = session['username']
    db['user_data'].update_one({'_id': username}, {'$set': {'v_contest_start_time': v_contest_start_time , 'is_running' : True}})
    return redirect(url_for('contest_page',contest_code = contest_code, username = username, contest_code_display = True))

@app.route("/add_friend" , methods = ['GET'])
def add_friend():

    username = session['username']
    user_data = db['user_data'].find({'_id':username})
    user_data = user_data[0]

    headers = {
    'content-type': 'application/json',
    'Authorization': 'Bearer {}'.format(user_data["access_token"])
    }

    name = request.args.get('username1')
    url = "https://api.codechef.com/users/" + name
    data = requests.get(url=url,headers=headers)
    data = data.json()
    isvalid = False
    if(data['result']['data']['code'] == 9001):
        isvalid = True    
        fullname = data['result']['data']['content']['fullname']
        friends = user_data['friends']
        if [name,fullname] not in friends and name not in [username]:
            # print(name)
            friends.append([name , fullname])
            db['user_data'].update_one({'_id': username}, {'$set': {'friends': friends}})
    if(isvalid == False):
        flash('Oh snap! No such user exists.')
    return redirect(url_for('friends'))

@app.route("/delete_friend" , methods = ['GET'])
def delete_friend():
    username = session['username']
    user_data = db['user_data'].find({'_id':username})
    user_data = user_data[0]
    name = request.args.get('username')
    friends = user_data['friends']
    for i in range(0 , len(friends)):
        if friends[i][0] == name:
            del friends[i:i+1]
            break
    db['user_data'].update_one({'_id': username}, {'$set': {'friends': friends}})
    return redirect(url_for('friends'))

@app.route("/compare", methods=['GET'])
def compare():
    compare_with = request.args.get("compare_with")
    contestcode = request.args.get("contestcode")

    u1data= compare_results(compare_with, contestcode , datetime.datetime.now())
    username = session['username']
    return render_template("compare.html", username = username, u1data = u1data, compare_with = compare_with, contestcode = contestcode)

@app.route("/end_contest")
def end_contest():
    username = session['username']
    user_data = db['user_data'].find({'_id':username})
    db['user_data'].update_one({'_id': username}, {'$set': {'problems' : list() , 'contest_start_time' : None , 'contest_end_time' : None , 'duration' : None , 'contest_code' : None , 'contest_name' : None , 'v_contest_start_time' : None , 'is_running' : False    ,'submissions' : dict()}})
    return redirect(url_for('main_page'))



if __name__ == "__main__":
    app.secret_key = "this is super secret wanna lubba dub dub"
    app.run(debug=True)
