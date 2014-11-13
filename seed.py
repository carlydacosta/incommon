import model
from model import InvestmentCompany, PortfolioCompany
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
	pass

	
if __name__ == "__main__":
	main()	