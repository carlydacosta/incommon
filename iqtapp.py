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

	sutter_hill_info = requests.get("http://api.crunchbase.com/v/2/organization/sutter-hill-ventures/investments?user_key=f0e2f7c3fd87b6dc6bc38c5ec8e7baf7")

	iqt_info = requests.get("http://api.crunchbase.com/v/2/organization/in-q-tel/investments?user_key=f0e2f7c3fd87b6dc6bc38c5ec8e7baf7")

	iqt_dict = iqt_info.json()
	sutter_hill_dict = sutter_hill_info.json()

	list_of_iqt_investment_items = iqt_dict["data"]["items"]
	list_of_sutter_investment_items = sutter_hill_dict["data"]["items"]
		
	iqt_portfolio_companies = {"name": [item["invested_in"]["name"] for item in list_of_iqt_investment_items]}			
	sutter_portfolio_companies = {"name": [item["invested_in"]["name"] for item in list_of_sutter_investment_items]}
	common_investments = [item for item in set(iqt_portfolio_companies["name"]) & set(sutter_portfolio_companies["name"])]  ## THIS IS AN AMAZING TIME SAVER!!!
				
	
	return render_template("index.html",
		common_investments=common_investments)


if __name__ == "__main__":
	app.run(debug=True)