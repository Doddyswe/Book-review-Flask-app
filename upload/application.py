import sys
import os
import psycopg2
from goodreads import *

from flask import Flask, session, render_template, redirect, url_for, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Init DATABASE_URL var
DATABASE_URL = os.environ["DATABASE_URL"]

app = Flask(__name__)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Init connect-to-db var conn 
conn = psycopg2.connect(DATABASE_URL, sslmode="require")
# Set up database
#engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))
db = conn.cursor()


# Data views

# Page views

    # Index
@app.route("/")
def index(message=None):
        if session.get("login") is None:
            session["login"]=False
        if session.get("login") == True:
            return redirect("/search")
        return render_template("home.html",message=message)

    # Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    message = None
    if request.method == "POST":
        userName = request.form.get("username")
        pw = request.form.get("password")
        db.execute("SELECT username,password FROM accounts where username = %s",(userName,))
        if db.fetchall() != []:
            message="That name is not available."
        else:
            db.execute("INSERT INTO accounts (username,password) VALUES (%s,%s)",(userName,pw))
            conn.commit()
            session["login"] = True
            session["username"] = userName
            return redirect("/search")
    return render_template("signup.html")

    # Login
@app.route("/login", methods=["GET", "POST"])
def login():
	if session.get("login") == False:
		message = None
		if request.method == "POST":
			userName = request.form.get("username")
			pw = request.form.get("password")
			db.execute("SELECT * FROM accounts WHERE username = %s and password =%s",(userName,pw))
			if db.fetchall() == []:
				message="You entered the wrong username or password."
			else:
				session["login"] = True
				session["username"] = userName
				return redirect('/search')
		return render_template("login.html",message=message)
	return redirect('/search')

    # Search
@app.route("/search", methods=["GET", "POST"])
def search():
	message = None
	res = None
	if request.method == "POST":
		isbn = request.form.get("isbn",None)
		author = request.form.get("author",None)
		title = request.form.get("title",None)
		if isbn:
			res = make_request(param=isbn)
		elif author:
			res = make_request(param=author)
		elif title:
			res = make_request(param=title)
		else:
			message="Please fill one of the forms."
		print(res[0], file=sys.stdout)
	return render_template("search.html",message=message,res=res)

    # Book
@app.route("/book/<code>", methods=["GET", "POST"])
def book(code):
    reviews = None
    check = True
    session["book_id"] = code
    if request.method == "POST" and can_review():
            message = request.form.get("message")
            db.execute("INSERT INTO reviews (book_id,review,acc_id) VALUES (%s,%s,(SELECT id FROM accounts WHERE username=%s))",(session['book_id'],message,session["username"]))
            conn.commit()
		
    if request.method == 'GET' or check:
            db.execute("SELECT review,acc_id FROM reviews WHERE book_id=%s",(session['book_id'],))
            reviews = db.fetchall()
            duzen = {}
            print(session.get("book_id"), file=sys.stdout)
            for rev in reviews:
                    acc_id = rev[1]
                    db.execute("SELECT username FROM accounts WHERE id=%s",(acc_id,))
                    user_name = db.fetchall()
                    duzen[user_name[0][0]] = rev[0]
            reviews = duzen
            print(reviews, file=sys.stdout)
    res = get_reviews(code)
    return render_template("book.html")

    # About
@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

    # Logout
@app.route("/logout")
def logout():
    session["login"] = False
    return render_template("logout.html")

# Functions, Classes and Objects
    # Enable review
def can_review():
    userName = session.get("username")
    book_id = session.get()



""" # nameCheck
if __name__ == "__main__":
    app.run()
 """