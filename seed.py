import model, sample
from model import InvestmentCompany, PortfolioCompany, VCList
from datetime import datetime

DATA="data"
ITEMS="items"
PATH="path"
PROPERTIES="properties"
RELATIONSHIPS="relationships"
HEADQUARTERS="headquarters"


def load_investment_company(vc_data):
	
	# Query the Database for the uuid
	uuid = model.session.query(InvestmentCompany).filter_by(uuid = vc_data["uuid"]).first()
	# If the uuid is already in the Database, do nothing
	if uuid:
		print "Investment Company already in the Database."
		return

	# If the uuid is not in the Database, then assign the company data to variables
	uuid = vc_data["uuid"]
	permalink = vc_data[PROPERTIES]["permalink"]
	name = vc_data[PROPERTIES]["name"]
	homepage_url = vc_data[PROPERTIES]["homepage_url"]
	
	if "founded_on" in vc_data[PROPERTIES]:
		founded = datetime.strptime(vc_data[PROPERTIES]["founded_on"], '%Y-%m-%d')

	description = vc_data[PROPERTIES]["short_description"]
	number_of_investments = vc_data[PROPERTIES]["number_of_investments"]
	city = vc_data[RELATIONSHIPS][HEADQUARTERS][ITEMS][0]["city"]
	state = vc_data[RELATIONSHIPS][HEADQUARTERS][ITEMS][0]["region"]

	# Create an investment company in the DB
	investmentcompany = model.InvestmentCompany(
		uuid=uuid,
		permalink=permalink, 
		name=name, 
		homepage_url=homepage_url,
		founded=founded,
		description=description,
		number_of_investments=number_of_investments,
		city=city,
		state=state)

	# Add it to the session
	model.session.add(investmentcompany)
	# Commit the session
	model.session.commit()

	print "Investment Company added to the Database."


def load_portfolio_company(pc_data):
	# Query the Database for the uuid
	uuid = model.session.query(PortfolioCompany).filter_by(uuid = pc_data["uuid"]).first()

	# If the uuid is already in the Database, do nothing
	if uuid:
		print "Portfolio Company already in the Database."
		return

	# If the uuid is not in the Database, then assign the company data to variables	
	uuid = pc_data["uuid"]
	permalink = pc_data[PROPERTIES]["permalink"]
	company_name = pc_data[PROPERTIES]["name"]
	
	if "headquarters" in pc_data[RELATIONSHIPS]:
		city = pc_data[RELATIONSHIPS][HEADQUARTERS][ITEMS][0]["city"]
		state = pc_data[RELATIONSHIPS][HEADQUARTERS][ITEMS][0]["region"]
	else:
		city = None
		state = None

	
	if "homepage_url" in pc_data[PROPERTIES]:
		homepage_url = pc_data[PROPERTIES]["homepage_url"]

	else:
		homepage_url = None
		
	if "founded_on" in pc_data[PROPERTIES]:
		founded = datetime.strptime(pc_data[PROPERTIES]["founded_on"], '%Y-%m-%d')
	else:
		founded = None

	total_funding = pc_data[PROPERTIES]["total_funding_usd"]
	
	if "short_description" in pc_data[PROPERTIES]:
		description = pc_data[PROPERTIES]["short_description"]
	else:
		description = None
	
	# Create an investment company in the DB
	portfoliocompany = model.PortfolioCompany(
		uuid=uuid,
		permalink=permalink,
		company_name=company_name,
		city=city,
		state=state,
		homepage_url=homepage_url,
		founded=founded,
		total_funding=total_funding,
		description=description)

	# Add it to the session
	model.session.add(portfoliocompany)
	# Commit it to the session
	model.session.commit()
	print "Portfolio Company added to the Database."


# This seed function relies on having memcache data.
def load_vc_list():

	mc = sample.memcache.Client(['127.0.0.1:11211'], debug=0)

	for page in range(1, 19):
		print "Page: ", page
		print "Getting info from memcache..."
		# get info from memcache by page
		vc_page = mc.get("vc_list_"+str(page))

		print "Iterating through VCs..."
		# each page has list of vc
		for vc in vc_page["items"]:
			# Query the Database for the name
			name = model.session.query(VCList).filter_by(name = vc["name"]).first()

			# If the name is already in the Database, do nothing
			if name:
				print "VC already in the Database."

			# If the name is not in the Database, then enter it	
			else:
				vc = model.VCList(
					name = vc["name"],
					permalink = vc["path"])
				print "Added VC to database."
				# Add it to the session
				model.session.add(vc)
	
	# Commit it to the session
	model.session.commit()
	print "VCs added to the Database."

def load_iqt_vc_partners():
	
	f = open("iqt_partners.csv").read()
	vc_partner_list = f.strip().split('\r')

	for vc_partner in vc_partner_list:

		path = vc_partner.lower().replace(" ", "-")

		iqtpartner = model.IqtPartner(
					name=vc_partner,
					permalink=path)

	 	model.session.add(iqtpartner)

	model.session.commit()


def main():
	load_vc_list()

	
if __name__ == "__main__":
	main()	