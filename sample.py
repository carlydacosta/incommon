import memcache, requests, os, model, seed, sample

#import json, ast
#from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
#from datetime import datetime
#from google.appengine.api import memcache

#establish memcache connection
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

#configuration

DATA="data"
ITEMS="items"
PATH="path"
PROPERTIES="properties"
RELATIONSHIPS="relationships"
HEADQUARTERS="headquarters"

#f0e2f7c3fd87b6dc6bc38c5ec8e7baf7


def check_for_vc(vc1_path):   # Need to add 2nd path
	print "Recieved path: ", vc1_path
	
	if not mc.get(vc1_path):
		print "Memcache result:",mc.get(vc1_path),". Checking database..."

		if model.session.query(model.InvestmentCompany).filter_by(permalink=vc1_path).all() == None:
			print "Database result: ",model.session.query(model.InvestmentCompany).filter_by(permalink=vc1_path).all(),". Making API request..."	 
		
			crunchbase = sample.Crunchbase()
			vc_data = crunchbase.get_vc_data(vc1_path)
			print "Recieved VC data", vc_data

			mc.set(vc1_path, vc_data)
			print "VC added data to memcache."
			
			seed.load_investment_company(vc_data)
			print "VC added to database."
	else:
		mc.get(vc1_path)
		print "Got VC from memcache."

	# call common_investments()


def common_investments(vc1_path):	# make for 2 paths

	if not mc.get("vc_portfolio"):
		print "Making API call..."

		crunchbase = Crunchbase()

		vc1_portfolio_list = crunchbase.get_vc_portfolio(vc1_path)
		#vc2_portfolio_list = crunchbase.get_vc_portfolio(vc2_path)

		mc.set("vc_portfolio", vc1_portfolio_list)  #how do I make keys unique?
		print "Set in memcache"
		#mc.set(vc2_path+"portfolio list", vc2_portfolio_list)

	else:
		vc_list = mc.get("vc_portfolio")
		print "Got from memcache..."

	for item in vc_list:
		pc = item["invested_in"]["name"]
		print "memcache result", pc

	# set(vc1_portfolio_list["invested_in"]["name"] for item in vc1_portfolio_list)
	# print "VC 1 Portfolio from crunchbase:", vc1_set
	
	# vc2_portfolios = set(vc2_portfolio_list["invested_in"]["name"] for item in vc2_portfolio_list)
	# print "VC 2 Portfolio from crunchbase:", vc2_set

	# common_investments_list = [item for item in set(vc1_set) & set(vc2_set)]  
	# print "Found common investments"

	# check_for_pc(common_investments_list)

	# return common_investments_list	

def check_for_pc(common_investments_list):
	pass
	#do what i did to check for vc company
	print "Recieved common investments."
	
	if not mc.get(vc1_path):
		print "Memcache result:",mc.get(vc1_path),". Checking database..."

		if model.session.query(model.InvestmentCompany).filter_by(permalink=vc1_path).all() == None:
			print "Database result: ",model.session.query(model.InvestmentCompany).filter_by(permalink=vc1_path).all(),". Making API request..."	 
		
			crunchbase = sample.Crunchbase()
			vc_data = crunchbase.get_vc_data(vc1_path)
			print "Recieved VC data", vc_data

			mc.set(vc1_path, vc_data)
			print "VC added data to memcache."
			
			seed.load_investment_company(vc_data)
			print "VC added to database."
	else:
		mc.get(vc1_path)
		print "Got VC from memcache."

'''
goal: 

c = CompareVcs('sutter-hill-ventures', 'sequoia')

companies = c.compare_investments()

data = {}
#TODO - make this comparison part of the VC class? 
for company in companies:
	company_object = Company(company)
	data[company] = company_object.get_data()

# Now you have a dictionary of company -> data

'''


class CompareVcs():

	def __init__(self, vc1, vc2):
		# check if same. How do you want to handle that?
		# self.vc1 = VC(vc1)
		# self.vc2 = VC(vc2)
		pass
	def compare_investments(self):
		# i_1 = self.vc1.get_investments()
		# i_2 = self.vc2.get_investments()
		# compare
		# Return a list of companies
		pass

class Company():
	def __int__(self, company_path):
		# Copy everything VC. Make a crunchbase call in that class for company.
		pass
	def get_data(self):
		# Do same cache as VC
		# Return data
		pass

class VC():

	def __init__(self, vc_path):
		# if VC path is none give error
		self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)
		self.vc_path = vc_path
		self.vc_data_key = "data-%s" % vc_path
		self.vc_investments_key = "investments-%s" % vc_path

	def get_data(self):
		# Is data in cache?
		cache = self.mc.get(self.vc_data_key)
		if cache is not None:
			return cache

		c = Crunchbase()

		data = c.get_vc_data(self.vc_path)
		self.mc.set(self.vc_data_key, data)
		return data

	def get_investments(self):
		
		cache = self.mc.get(self.vc_investments_key)
		if cache is not None:
			return cache

		c = Crunchbase()

		data = c.get_vc_portfolio(self.vc_path)
		self.mc.set(self.vc_investments_key, data)

	
class Crunchbase():
	URL_BASE = "http://api.crunchbase.com/v/2/"
	def __init__(self):
		self.API_KEY = os.environ.get('CRUNCHBASE_API_KEY')
		# this.API_SECRET_KEY = os.environ.get('APP_SECRET_KEY')

	def get_vc_data(self, vc_path):
		return self._query(vc_path, "")
		
	def get_vc_portfolio(self, vc_path):
		return self._query(vc_path, "/investments")	

	def _query(self, vc_path, target=""):
		print "Queried Crunchbase"
		response = requests.get(self.URL_BASE + "organization/" + vc_path + target + "?user_key=" + self.API_KEY)

		if response.status_code is not 200:
			print "Failed lookup: %d" % vc_portfolio.status_code
			return None
		return response.json()['data']



# def iqt_vc_partners_list():
	
# 	f = open("iqt_partners.csv")
# 	vc_partner_list = f.strip().split('/r')

# 	return vc_partner_list

def main():
	#check_for_vc("in-q-tel")
	common_investments("sutter-hill-ventures")

	

if __name__ == "__main__":
	main()				
