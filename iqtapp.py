from flask import Flask, request, session, redirect, json, render_template, Response
from model import User, VCList, PortfolioCompany, IqtDetail, session as dbsession
import os
import sample
import datetime


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
	
	print vc1, vc2, "what i am getting!!!!!!!!"
	#query database for path
	vc1_object = dbsession.query(VCList).filter_by(name = vc1).first()
	vc1_path = vc1_object.permalink.encode("utf8")
	
	vc2_object = dbsession.query(VCList).filter_by(name = vc2).first()
	vc2_path = vc2_object.permalink.encode("utf8")
	#use path to call the functions that return the common investments list
	vc = sample.CompareVcs(vc1_path, vc2_path)
	common_investments_list = list(vc.compare_investments())
	
	#create a list of dictionaries [{item1 name: , item1 id: }]
	#
	# common_investments_dict = [{"name":, "id"}

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
							total_funding=pc.total_funding)

@app.route("/ajax/iqt-company-detail", methods=['GET'])
def show_iqt_company_details():

	pc_name = request.args.get("company")
	print pc_name
	# check for company name in iqtdetail table
	company_object = dbsession.query(IqtDetail).filter_by(pc_name=pc_name)
	print company_object

	if company_object:
		iqtpartner_first_name = company_object.partner_first_name
		iqtpartner_last_name = company_object.partner_last_name
		equity_percent_first_trans = company_object.equity_percent_first_trans
		equity_percent_second_trans = company_object.equity_percent_second_trans
		ownership_percent = company_object.ownership_percent

		return render_template("iqt_pc_detail.html",
						iqtpartner_first_name=iqtpartner_first_name,
						iqtpartner_last_name=iqtpartner_last_name,
						equity_percent_first_trans=equity_percent_first_trans,
						equity_percent_second_trans=equity_percent_second_trans,
						ownership_percent=ownership_percent)


@app.route("/log-out", methods=['POST'])
def log_out():

    session["user"] = {}
    return "/"


if __name__ == "__main__":
	app.run(debug=True)

