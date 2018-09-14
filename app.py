from flask import Flask, render_template, jsonify

from api_return_scripts import *

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template("home.html")

@app.route("/contestpage/<contest_code>")
def contest_page(contest_code):
    # x = return_contest_details(contest_code)
    # print(x)
    x = {'name': 'January Cook-Off 2018', 'start_date': '2018-01-21 21:30:00', 'end_date': '2018-01-22 00:00:00', 'problems': ['FINDA', 'MAGA', 'MULTHREE', 'FARGRAPH', 'SURVIVE']}
    fmt = '%Y-%m-%d %H:%M:%S'
    s_d = datetime.datetime.strptime(x['start_date'], fmt)
    e_d = datetime.datetime.strptime(x['end_date'], fmt)
    print(s_d, e_d)
    diff = e_d - s_d
    diff = diff.total_seconds()/60

    return render_template("contestpage.html",contest_code = contest_code, name = x['name'], mins = diff, problems = x['problems'])

@app.route("/standings")
def current_standing():
	obj=[
    {
        "id" : "001",
        "name" : "apple",
        "category" : "fruit",
        "color" : "red"
    },
    {
        "id" : "002",
        "name" : "melon",
        "category" : "fruit",
        "color" : "green"
    },
    {
        "id" : "003",
        "name" : "banana",
        "category" : "fruit",
        "color" : "yellow"
    }
	] 
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


if __name__ == "__main__":
	app.run(debug=True)