from flask import Flask, request, session, redirect, json, render_template, flash, jsonify
from model import User, PastQueries, VCList, session as dbsession
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
	# session.clear()
	# print session["user"]
	print session
	if user:
		session["user"] = user.email
		return redirect("/vc-list") 
	# if user is not in the db, ask them to sign up
	else:
		print "at else"
		
		return redirect("/")  # note i can send the return /index to javascript vs redirect it



@app.route('/new-user', methods=['POST'])  # route here if click signup button on main page
def process_new_user():
	# session.clear()
	
	first_name = request.form.get('first-name')
	last_name = request.form.get('last-name')
	user_email = request.form.get('new-user-email')
	password = request.form.get('new-user-password')
	user = User(
		first_name = first_name,
		last_name = last_name,
		email = user_email,
		password=password
		)
	# user.hash_password(password)
	
	if dbsession.query(User).filter_by(email = user_email).first():
		
		return redirect('/')  # note i can send the return /index to javascript vs redirect it
	
	else:
		dbsession.add(user)
    	dbsession.commit()
    	session["user"] = user.email
    	return redirect("/vc-list")  # note i can send the return /index to javascript vs redirect it


@app.route("/vc-list")
def index():
		
	return render_template("vc_list.html")


@app.route("/common_investments", methods=['GET'])  # route here when the 'find common investments' button is selected
def show_common_investments():
	#get company names from form
	vc1 = request.args.get("vc1-list")
	vc2 = request.args.get("vc2-list")
	# print "printing vc1 and 2 #################: ", vc1, vc2
	#query database for path
	vc1_object = dbsession.query(VCList).filter_by(name = vc1).first()
	# print vc1_object
	vc1_path = vc1_object.permalink.encode("utf8")
	# print vc1_path

	vc2_object = dbsession.query(VCList).filter_by(name = vc2).first()
	vc2_path = vc2_object.permalink.encode("utf8")
	#use path to call the functions that return the common investments list
	vc = sample.CompareVcs(vc1_path, vc2_path)
	common_investments_set = vc.compare_investments()

	print "Flask common investments!!!!!!!!!!!!!!!!", common_investments_set
	
	return render_template("vc_list.html",
						common_investments_set=common_investments_set)

@app.route("/log-out", methods=['POST'])
def log_out():

    session["user"] = {}
    return "/"  # if I just return this, then I can use it in javascript.  Versus return redirect ('/') would just be used internal to flask and send me


if __name__ == "__main__":
	app.run(debug=True)

