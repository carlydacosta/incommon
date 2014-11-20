from flask import Flask, request, session, redirect, json, render_template, Response
from model import User, VCList, session as dbsession
import os
import sample


# configuration
APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')


app = Flask(__name__)
app.secret_key = APP_SECRET_KEY


@app.route('/', methods=['GET'])
def main_page():
	
	return render_template("main.html")


@app.route('/login', methods=['POST'])
def process_login():
	
	user_email = request.form.get('user-email')
	password = request.form.get('user-password')
	
	user = dbsession.query(User).filter_by(password=password).filter_by(email=user_email).first()
	# session.clear()
	# print session["user"]
	print session
	
	if user:
		session["user"] = user.email
		return redirect("/vc-list") 
	
	else:
		print "at else"
		return redirect("/")



@app.route('/new-user', methods=['POST'])
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


@app.route("/ajax/common-investments", methods=['GET'])  # route here when the 'find common investments' button is selected
def show_common_investments():
	#get company names from form
	vc1 = request.args.get("vc1")
	vc2 = request.args.get("vc2")
	print "printing vc1 and 2 #################: ", vc1, vc2
	#query database for path
	vc1_object = dbsession.query(VCList).filter_by(name = vc1).first()
	print vc1_object
	vc1_path = vc1_object.permalink.encode("utf8")
	print vc1_path

	vc2_object = dbsession.query(VCList).filter_by(name = vc2).first()
	vc2_path = vc2_object.permalink.encode("utf8")
	#use path to call the functions that return the common investments list
	vc = sample.CompareVcs(vc1_path, vc2_path)
	common_investments_set = list(vc.compare_investments())

	print "Flask common investments!!!!!!!!!!!!!!!!", common_investments_set
	
	r = json.dumps(list(common_investments_set))
	return Response(r, mimetype="text/json")
	# return render_template("common_investments.html",
	# 					common_investments_set=common_investments_set)

@app.route("/log-out", methods=['POST'])
def log_out():

    session["user"] = {}
    return "/"


if __name__ == "__main__":
	app.run(debug=True)

