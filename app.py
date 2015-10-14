from flask import Flask, render_template, session
from flask import redirect, url_for
import sqlite3;
import utils

app = Flask(__name__)

@app.route("/login")
def login():
	return render_template("login.html");

@app.route("/home")
def home():
	conn = sqlite3.connect('data.db')
	cur = conn.cursor()
	q = "SELECT * FROM posts"
	cur.execute(q)
	all_rows = cur.fetchall()
        print all_rows
	return render_template("home.html", all_rows=all_rows)

@app.route("/")
def index():
    return "hello"


if __name__ == "__main__":
   app.debug = True
   app.run(host='0.0.0.0', port=8000)
