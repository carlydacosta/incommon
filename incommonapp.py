from flask import Flask, request, session, redirect, render_template
from table_class_objects import User, VCList, PortfolioCompany, session as dbsession
import os
import class_objects

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
	
	user = dbsession.query(User).filter_by(email=user_email).first()
	
	if user and user.check_password(password):
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
	
	user.set_password(password)
	
	if dbsession.query(User).filter_by(email = user_email).first():
		
		return redirect('/')
	
	else:
		dbsession.add(user)
    	dbsession.commit()
    	session["user"] = user.email
    	return redirect("/vc-list")


@app.route("/vc-list")
def index():
		
	return render_template("vc_list.html")


@app.route("/ajax/common-investments", methods=['GET'])  # route here when the 'find common investments' button is selected
def show_common_investments():
	
	#get company names from form
	vc1 = request.args.get("vc1")
	vc2 = request.args.get("vc2")
	
	#query database for path
	vc1_object = dbsession.query(VCList).filter_by(name = vc1).first()
	vc1_path = vc1_object.permalink.encode("utf8")
	
	vc2_object = dbsession.query(VCList).filter_by(name = vc2).first()
	vc2_path = vc2_object.permalink.encode("utf8")
	
	#use path to call the functions that return the common investments list
	vc = class_objects.CompareVcs(vc1_path, vc2_path)
	common_investments_list = list(vc.compare_investments())

	return render_template("common_investments.html",
						common_investments_list=common_investments_list)


@app.route("/ajax/company-data", methods=['GET'])
def show_company_data():
	
	pc_name = request.args.get("company")

	#get company name
	pc = dbsession.query(PortfolioCompany).filter_by(company_name = pc_name).first()

	date_string = pc.founded.strftime("%B %d, %Y")
	 
	return render_template("company_data.html",
							description=pc.description,
							founded=date_string,
							homepage_url=pc.homepage_url,
							city=pc.city,
							state=pc.state,
							total_funding=format_currency(pc.total_funding))


@app.route("/log-out", methods=['POST'])
def log_out():

    session["user"] = {}
    return "/"

def format_currency(value):
    return "${:,}".format(value)

if __name__ == "__main__":
	app.run(debug=True)

