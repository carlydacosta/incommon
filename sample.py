import requests, os, model, json #ast?


# configuration
CRUNCHBASE_API_KEY = os.environ.get('CRUNCHBASE_API_KEY')
APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')

DATA="data"
ITEMS="items"
PATH="path"
PROPERTIES="properties"
RELATIONSHIPS="relationships"
HEADQUARTERS="headquarters"


def main():

	portfolio_company_uuids = set()
	sectors_set = set()

##############  Instantiating Investment Companies ###############	
	
	# request a list of investment company paths (i.e. permalinks)
	investment_companies = requests.get("http://api.crunchbase.com/v/2/organizations?organization_types=investor&user_key="+str(CRUNCHBASE_API_KEY)).json()[DATA][ITEMS]

	for company in investment_companies:
		# get the path to call investment company details
		permalink = company[PATH]

		icompany_data = requests.get("http://api.crunchbase.com/v/2/"+permalink+"?user_key="+str(CRUNCHBASE_API_KEY)).json()[DATA]
		
		name = icompany_data[PROPERTIES]["name"]
		homepage_url = icompany_data[PROPERTIES]["homepage_url"]
		founded = icompany_data[PROPERTIES]["founded_on"]
		description = icompany_data[PROPERTIES]["short_description"]
		number_of_investments = icompany_data[PROPERTIES]["number_of_investments"]
		city = icompany_data[RELATIONSHIPS][HEADQUARTERS][ITEMS][0]["city"]
		state = icompany_data[RELATIONSHIPS][HEADQUARTERS][ITEMS][0]["region"]

		investmentcompany = model.InvestmentCompany(
			permalink=permalink, 
			name=name, 
			homepage_url=homepage_url,
			founded=founded,
			description=description,
			number_of_investments=number_of_investments,
			city=city,
			state=state)

		model.session.add(investmentcompany)

		#use investmentcompany.id for when investmentcompany_id is in a column
		
		
	##############  Instantiating Portfolio Companies ###############		

		#create portfolio company instance
		for item in icompany_data[RELATIONSHIPS]["investments"][ITEMS]:	

			uuid = pcompany_data["uuid"]
			
			if uuid not in portfolio_company_uuids:		
				# get the path to call portfolio company details
				pc_permalink = item["invested_in"][PATH]   
			
				pcompany_data = requests.get("http://api.crunchbase.com/v/2/"+pc_permalink+"?user_key="+str(CRUNCHBASE_API_KEY)).json()[DATA]
							
				company_name = pcompany_data["name"]
				city = pcompany_data[RELATIONSHIPS][HEADQUARTERS][ITEMS][0]["city"]
				state = pcompany_data[RELATIONSHIPS][HEADQUARTERS][ITEMS][1]["region"]
				homepage_url = pcompany_data["homepage_url"]
				founded = pcompany_data["founded_on"]
				total_funding = pcompany_data["total_funding_usd"]
				description = pcompany_data["short_description"]

				portfoliocompany = model.PortfolioCompany(
					permalink=permalink,
					company_name=company_name,
					city=city,
					state=state,
					homepage_url=homepage_url,
					founded=founded,
					total_funding=total_funding,
					description=description)

				model.session.add(portfoliocompany)

				portfolio_company_uuids.add(uuid)
		
	##############  Instantiating Investment Company Partners ###############	
		
		# create parter instance with data available in details
		for partner in icompany_data[RELATIONSHIPS]["current_team"]:
			
			partner = model.Partner(
				first_name=partner["first_name"],
				last_name=partner["last_name"],
				title=partner["title"],
				investmentcompany_id=investmentcompany.id)
			
			model.session.add(partner)
		

	# ##############  Instantiating Investment Company Sector Focuses ###############

		# create sector focus instance with data available in details
		for sector in icompany_data[PROPERTIES]["sectors"]:
			
			if sector not in sectors_set:

				sector = model.SectorFocus(sector=sector)
				
				model.session.add(sectorfocus)

				sectors_set.add(sector)
		

	model.session.commit()


	# common_investments = [item for item in set(investmentcompany1) & set(investmentcompany2)]  ## THIS IS AN AMAZING TIME SAVER!!!

if __name__ == "__main__":
	main()				

############
	#investment company details through permalink
		# metadata
		# data
			# properties
				# homepage_url
				# short descript
				# founded_on
				# number_of_investments
				# sectors   ------> use for sector focus
					# items
				
			# relationships
				# founders
					# items
				# current team  -----> use for partners
					# items
						# first_name
						# last_name
						# title
				# headquarters
					# items
						# city
						# region (shows state)
				# investments
					# items
						# invested_in
							# name
							# path (PERMALINK!)  -------> use to look up company

				# websites (linkedin twitter etc) ---> use for later
					# items
				# news  ------> use for later
					# items

#portfolio company details through permalink
		# metadata
		# data
			# uuid
			# properties
				# name
				# homepage_url
				# short descript
				# founded_on
				# sectors   ------> use for sector focus
				# number_of_investments
				# total_funding_usd (not formatted, just integers)
			# relationships
				# founders
					# items
				# headquarters
					# items
						# city
						# region (shows state)
				# funding_rounds
					# items
						# path -------> use to look up funding round details
				# categories
					# items
						# name  ------> use for category
				# primary_image
					# items
						# path ----> url to the image
				# websites (linkedin twitter etc) ---> use for later
					# items
				# news  ------> use for later
					# items	
	