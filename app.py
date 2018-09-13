from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template("home.html")

@app.route("/contestpage")
def contest_page():
    return render_template("contestpage.html")


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

if __name__ == "__main__":
	app.run(debug=True)