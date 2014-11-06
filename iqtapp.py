from flask import Flask, render_template
import os, requests


# configuration
CRUNCHBASE_API_KEY = os.environ.get('CRUNCHBASE_API_KEY')
APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')



app = Flask(__name__)

@app.route("/")
def index():
	#get a list of investor companies from CB
	#for each company, get a list of their portfolio companies

	list_of_sutter_investment_items = requests.get("http://api.crunchbase.com/v/2/organization/sutter-hill-ventures/investments?user_key=CRUNCHBASE_API_KEY").json()["data"]["items"]

	list_of_iqt_investment_items  = requests.get("http://api.crunchbase.com/v/2/organization/in-q-tel/investments?user_key=CRUNCHBASE_API_KEY").json()["data"]["items"]
		
	iqt_portfolio_companies = {"name": [item["invested_in"]["name"] for item in list_of_iqt_investment_items]}			
	sutter_portfolio_companies = {"name": [item["invested_in"]["name"] for item in list_of_sutter_investment_items]}
	common_investments = [item for item in set(iqt_portfolio_companies["name"]) & set(sutter_portfolio_companies["name"])]  ## THIS IS AN AMAZING TIME SAVER!!!
				
	
	return render_template("index.html",
		common_investments=common_investments)


if __name__ == "__main__":
	app.run(debug=True)