from flask import Flask, request, session, redirect, render_template, flash
from model import User, PastQueries, session as dbsession
import os, requests
import sample


# configuration
APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')



app = Flask(__name__)
app.secret_key = APP_SECRET_KEY

@app.route('/', methods=['GET'])
def main_page():
	
	# session['user'] = {}
	return render_template("main.html")  # show name/logo of app, log in fields & button, sign up fields & buttom



@app.route('/login', methods=['POST'])	# route here when click login button on main page
def process_login():
	print "at process_login"
	user_email = request.form.get('user-email')
	password = request.form.get('user-password')
	# check if user email and password are in db
	user = dbsession.query(User).filter_by(password=password).filter_by(email=user_email).first()
	# if user exists, add them to the flask session by userid
	print "after query", user
	session.clear()
	# print session["user"]
	print session
	if user:
		if user.email in session["user"]:
			pass
		else:
			session["user"] = user.email
		return redirect("/index") 
	# if user is not in the db, ask them to sign up
	else:
		print "at else"
		
		return redirect("/")  # note i can send the return /index to javascript vs redirect it



@app.route('/new-user', methods=['POST'])  # route here if click signup button on main page
def process_new_user():
	session.clear()
	
	first_name = request.form.get('first-name')
	last_name = request.form.get('last-name')
	user_email = request.form.get('new-user-email')
	password = request.form.get('new-user-password')
	user = User(
		first_name = first_name,
		last_name = last_name,
		email = user_email,
		password = password)
	
	if dbsession.query(User).filter_by(email = user_email).first():
		
		return redirect('/')  # note i can send the return /index to javascript vs redirect it

	
	else:
		dbsession.add(user)
    	dbsession.commit()
    	session["user"] = user.email
    	return redirect("/index")  # note i can send the return /index to javascript vs redirect it

@app.route("/log-out", methods=['POST'])
def log_out():

    session["user"] = {}
    return "/"  # if I just return this, then I can use it in javascript.  Versus return redirect ('/') would just be used internal to flask and send me


@app.route("/index")  # how do I send this to javascript?
def index():

	vc_list = [] # list of vc names is here

	return render_template("index.html",
							vc_list=vc_list)  # show 2 dropdown lists of vcs and 'find common investments' button


@app.route("/common_investments", methods=['GET'])  # route here when the 'find common investments' button is selected
def show_common_investments():
	
	# call the functions that return the common investments list
	# return the results to javascript
	return results
		


if __name__ == "__main__":
	app.run(debug=True)

