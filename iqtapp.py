from flask import Flask, request, session, redirect, render_template, flash, Markup
from model import User, PastQueries, session as dbsession
import os, requests
import sample.py


# configuration
APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')



app = Flask(__name__)

@app.route('/', methods=['GET'])
def main_page():
	
	session['user'] = {}
	return render_template("main.html")  # show name/logo of app, log in fields & button, sign up fields & buttom



@app.route('/login', methods=['POST'])	# route here when click login button on main page
def process_login():
	
	user_email = request.form['user_email']
	password = request.form['password']
	# check if user email and password are in db
	user = dbsession.query(User).filter_by(password=password).filter_by(email=user_email).first()
	# if user exists, add them to the flask session by userid
	if user:
		session['user_id'] = user.id
		return redirect("/index") 
	# if user is not in the db, ask them to sign up
	else:
		flash("Oops, we don't recognize that email / password combination. Give it another try or create an account here:"+ Markup("<h1><a href='/signup'>Signup</a></h1>"))
		return redirect("/login")



@app.route('/signup', methods=['POST'])  # route here if click signup button on main page
def process_new_user():
	
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	user_email = request.form['user_email']
	password = request.form['password']
	user = User(
		first_name = first_name,
		last_name = last_name,
		email = user_email,
		password = password)
	
	if dbsession.query(User).filter_by(email = user_email).first():
		flash("That email is already in use - you must have logged in before!  Log in here!"+ Markup("<h1><a href='/login'>Login</a></h1>"))
		return redirect('/signup')
	
	else:
		dbsession.add(user)
    	dbsession.commit()
    	session['user_id'] = user.id
    	return redirect("/index")

@app.route("/log-out", methods=['POST'])
def log_out():

    session["user"] = {}
    return "/"


@app.route("/choose_vcs", methods=['GET'])
def index():
	
	vc_list=[]
	# get vc_list

	return render_template("choose_vcs.html",
							vc_list=vc_list)


@app.route("/common_investments", methods=['GET'])
def show_common_investments():
	
	results = sample.common_investments()

	return results
		


if __name__ == "__main__":
	app.run(debug=True)

