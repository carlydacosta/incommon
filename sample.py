import requests, os, model, json #ast?


# configuration
CRUNCHBASE_API_KEY = os.environ.get('CRUNCHBASE_API_KEY')
APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')


def main():
	
	# request a list of investment companies
	investment_companies = requests.get("http://api.crunchbase.com/v/2/organizations?organization_types=investor&user_key="+str(CRUNCHBASE_API_KEY)).json()["data"]["items"]

	# investment company permalinks
	ic_permalinks = [item["path"] for item in investment_companies]	
	
	print "permalinks!", ic_permalinks[1:5]

	for item in investment_companies:
		
		investmentcompany = model.InvestmentCompany(permalink=item["path"], name=item["name"], )
		model.session.add(investmentcompany)

		print "instances of Investment Company", investmentcompany
		
		for item in ic_permalinks:
			# request individual investment company details using permalink
			ic_data = requests.get("http://api.crunchbase.com/v/2/"+item+"/investments?user_key="+str(CRUNCHBASE_API_KEY)).json()["data"]
			
			# creat investment company instance with data available in details
			investmentcompany = model.InvestmentCompany(homepage_url=ic_data["properties"]["homepage_url"], description=ic_data["properties"]["short_description"], founded=ic_data["properties"]["founded_on"], number_of_investments=ic_data["properties"]["number_of_investments"])
			model.session.add(investmentcompany)

			print "additions to investment company instances", investmentcompany
			
			for item in ic_data["relationships"]["headquarters"]:
				investmentcompany = model.InvestmentCompany(city=item["city"], state=item["region"])
				model.session.add(investmentcompany)
			print "made it through investment company"

			# create sector focus instance with data available in details
			for item in ic_data["properties"]["sectors"]:
				sectorfocus = model.SectorFocus(sector1=item[0], sector2=item[1], sector3=item[2])
				model.session.add(sectorfocus)
			print "made it through sectors"

			# create parter instance with data available in details
			for item in ic_data["relationships"]["current_team"]:
				partner = model.Partner(first_name=item["first_name"], last_name=item["last_name"], title=item["title"])
				model.session.add(partner)
			print "made it through partners"
							
			# portfolio company permalinks
			pc_permalinks = [item["invested_in"]["path"] for item in ic_data["relationships"]["investments"]]  
			# create portfolio company instance with data available in details
			for item in ic_data["relationships"]["investments"]:
				portfoliocompany = model.PortfolioCompany(name=item["invested_in"]["name"], permalink=item["invested_in"]["path"])
				model.session.add(portfoliocompany)

			print "company permalinks", pc_permalinks[1:5]	

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

	
#############