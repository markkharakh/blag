from flask import Flask, render_template, session, request
from flask import redirect, url_for
import sqlite3
import utils

app = Flask(__name__)

@app.route("/about")
def about():
        if usersession() == "":
                return redirect("/login")
        return render_template("about.html")
        
@app.route("/login", methods = ['GET','POST'])
def login():
        '''conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        q = "SELECT users.name FROM users"
        cur.execute(q)
        all_rows = cur.fetchall()
        print all_rows'''
        all_rows = utils.getAllUsers()
        for n in range(len(all_rows)):
                all_rows[n] = all_rows[n][0]
        if request.method == 'POST':
                user = str(request.form['user'])
                password = str(request.form['pass'])
                error = ""
                if request.form['press'] == "login":
                        if utils.authenticate(user,password):
                                session['user'] = user
                                return redirect("/home")
                        else:
                                error = "Incorrect Username or Password. Try Again."
                                return render_template("login.html",error=error)
                else:
                        print "a"
                        if user in all_rows:
                                error = "Username already exists. Please try another"
                                return render_template("login.html",error=error)
                        else: 
                                utils.addUser(user,password,1)
                                session['user'] = user
                                return redirect("/home")
        return render_template("login.html") #login failed

@app.route("/logout")
def logout():
        del session['user']
        return redirect("/login")

@app.route("/")
@app.route("/home")
def home():
        if usersession() == "":
                return redirect("/login")
        all_rows = utils.getAllPosts()
        return render_template("home.html", all_rows=all_rows)

@app.route("/post/<int:postid>", methods = ['GET','POST'])
def post(postid):
        if usersession() == "":
                return redirect("/login")
        if request.method == 'POST':
                content = str(request.form['name'])
                utils.writeComment(content, utils.getUserId(session['user']), postid)
        postrow = utils.getPost(postid)
        commentrow = utils.getCommentsOnPost(postid)
        users = []
        for comment in commentrow:
                users.append(comment[2])
        size = len(users)
        print commentrow
        print users
        return render_template("post.html", postrow = postrow, commentrow = commentrow, users = users, size = size)

@app.route("/makepost", methods = ['GET','POST'])
def makepost():
        if 'user' not in session:
                return redirect ("/login")
        if request.method == 'POST':
                title = request.form['title']
                content = request.form['content']
                user = session['user']
                idp = utils.writePost(title,content,utils.getUserId(user))
                return redirect("/post/"+str(idp))
        else:
                return render_template("newpost.html")

@app.route("/delete/<int:pid>")
@app.route("/delete/<int:pid>/<int:cid>")
def delete(pid=0,cid=0):
        if 'user' not in session:
                return redirect ("/login")
        if cid != 0 and utils.getComment(cid)[5] == session['user']:
                utils.deleteComment(cid)
                return redirect(url_for('post',postid=pid))
        elif pid != 0 and utils.getPost(pid)[5] == session['user']:
                utils.deletePost(pid)
        return redirect("/home")
        
@app.route("/user")
def user():
        return

@app.route("/")
def index():
        return "hello"

def upload(url):
        filename = ""
        return filename

def usersession():
        if session.has_key('user'):
                user = session['user']
        else:
                user = ""
        return user

if __name__ == "__main__":
        app.secret_key = "hello"
        app.debug = True
        app.run(host='0.0.0.0', port=8000)
        #app.run(debug=True)
