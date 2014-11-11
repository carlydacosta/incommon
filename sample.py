import requests, os, model, json, ast, session

# from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
#from datetime import datetime
#from google.appengine.api import memcache


# configuration
CRUNCHBASE_API_KEY = os.environ.get('CRUNCHBASE_API_KEY')
APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')

DATA="data"
ITEMS="items"
PATH="path"
PROPERTIES="properties"
RELATIONSHIPS="relationships"
HEADQUARTERS="headquarters"

#f0e2f7c3fd87b6dc6bc38c5ec8e7baf7




def common_investments(vc1_path, vc2_path):
	crunchbase = Crunchbase()
	vc1 = crunchbase.get_vc_portfolio(vc1_path)
	vc2 = crunchbase.get_vc_portfolio(vc2_path)


	common_investments = [item for item in set(vc1["name"]) & set(vc2["name"])]  ## THIS IS AN AMAZING TIME SAVER!!!
	
	print common_investments	


class Crunchbase():

	def get_vcs():

		vc_org_list = requests.get("http://api.crunchbase.com/v/2/organizations?organization_types=investor&user_key="+str(CRUNCHBASE_API_KEY)).json()[DATA][ITEMS]

		return vc_org_list

	def get_vc_data(self, vc_path):

		vc_data = requests.get("http://api.crunchbase.com/v/2/"+vc_path+"?user_key="+str(CRUNCHBASE_API_KEY)).json()[DATA]

		return vc_data
		

	def get_vc_portfolio(self, vc_path):

		vc_investment_list = requests.get("http://api.crunchbase.com/v/2/organization/"+vc_path+"/investments?user_key="+str(CRUNCHBASE_API_KEY)).json()[DATA][ITEMS]

		vc_portfolio_companies = {"name": [item["invested_in"]["name"] for item in vc_investment_list]}
		
		return vc_portfolio_companies

def iqt_vc_partners_list():
	
	f = open("iqt_partners.csv")
	vc_partner_list = f.strip().split('/r')

	return vc_partner_list

def main():
	common_investments("sutter-hill-ventures", "in-q-tel")

	# common_investments = [item for item in set(investmentcompany1) & set(investmentcompany2)]  ## THIS IS AN AMAZING TIME SAVER!!!

if __name__ == "__main__":
	main()				

