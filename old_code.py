def load_investmentcompanies():
	
	##############  Instantiating Investment Companies ###############	
	test_companies = ["sutter-hill-ventures", "in-q-tel"]
	
	# request a list of investment company paths (i.e. permalinks)
	investment_companies = requests.get("http://api.crunchbase.com/v/2/organizations?organization_types=investor&user_key="+str(CRUNCHBASE_API_KEY)+"&page=2").json()[DATA][ITEMS]

	for company in investment_companies[0:3]:
		# get the path to call investment company details
		permalink = company[PATH]

		response = requests.get("http://api.crunchbase.com/v/2/"+permalink+"?user_key="+str(CRUNCHBASE_API_KEY))

		icompany_data = response.json()[DATA]
		
		# pull info to create an investment company instance
		name = icompany_data[PROPERTIES]["name"]
		homepage_url = icompany_data[PROPERTIES]["homepage_url"]
		
		if "founded_on" in icompany_data[PROPERTIES]:
			founded = datetime.strptime(icompany_data[PROPERTIES]["founded_on"], '%Y-%m-%d')

		description = icompany_data[PROPERTIES]["short_description"]
		number_of_investments = icompany_data[PROPERTIES]["number_of_investments"]
		city = icompany_data[RELATIONSHIPS][HEADQUARTERS][ITEMS][0]["city"]
		state = icompany_data[RELATIONSHIPS][HEADQUARTERS][ITEMS][0]["region"]

		# create an investment company in the table
		investmentcompany = model.InvestmentCompany(
			permalink=permalink, 
			name=name, 
			homepage_url=homepage_url,
			founded=founded,
			description=description,
			number_of_investments=number_of_investments,
			city=city,
			state=state)

		# add it to the session
		model.session.add(investmentcompany)

		pcompany_permalinks = set()
		sectors_set = set()

		#############  Instantiating Portfolio Companies ###############		

		#need each item to get to the portfolio company path (permalink), which is used to get their details so I can create an instance
		for item in icompany_data[RELATIONSHIPS]["investments"][ITEMS]:	
			# get the permalink
			pc_permalink = item["invested_in"][PATH]
			# only want to create one instance of each portfolio company, so use permalink only once.  Check this be seeing if the link is already in the set established at the begining of the function
			if pc_permalink not in pcompany_permalinks:	

				response = requests.get("http://api.crunchbase.com/v/2/"+pc_permalink+"?user_key="+str(CRUNCHBASE_API_KEY))	
				
				pcompany_data = response.json()[DATA]
				
				# pull info to create a portfolio company instance			
				uuid = pcompany_data["uuid"]
				company_name = pcompany_data[PROPERTIES]["name"]

				if "headquarters" in pcompany_data[RELATIONSHIPS]:
					city = pcompany_data[RELATIONSHIPS][HEADQUARTERS][ITEMS][0]["city"]
					state = pcompany_data[RELATIONSHIPS][HEADQUARTERS][ITEMS][0]["region"]
				
				if "homepage_url" in pcompany_data[PROPERTIES]:
					homepage_url = pcompany_data[PROPERTIES]["homepage_url"]
					
				if "founded_on" in pcompany_data[PROPERTIES]:
					founded = datetime.strptime(pcompany_data[PROPERTIES]["founded_on"], '%Y-%m-%d')

				if "short_description" in pcompany_data[PROPERTIES]:
					description = pcompany_data[PROPERTIES]["short_description"]
				
				total_funding = pcompany_data[PROPERTIES]["total_funding_usd"]
				
				# create a portfolio company
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

				model.session.add(portfoliocompany)
				# since permalink used wasn't in the list, add it now so not used again
				pcompany_permalinks.add(pc_permalink)

		# 		##############  Instantiating Investment b/w Investment Company and Portfolio Company  ##############

		# 		# use pc data drill down to data/relashionship/funding_rounds/items
		# 		funding_rounds = pcompany_data[RELATIONSHIPS]["funding_rounds"][ITEMS]
		# 		# iterate through items to get path to funding round
		# 		for item in funding_rounds:

		# 			funding_round_permalink = item["path"]
									
		# 			response = requests.get("http://api.crunchbase.com/v/2/"+funding_round_permalink+"?user_key="+str(CRUNCHBASE_API_KEY))

		# 			if response.status_code != "<Response [200]>":
		# 				print funding_round_permalink
		# 				continue

		# 			# use path to request data on each funding round
		# 			funding_detail = response.json()[DATA][PROPERTIES]
		# 			# pull info to create an investment instance
					
		# 			if "money_raised" in funding_detail:

		# 				money_raised = funding_detail["money_raised"]

		# 			if "series" in funding_detail:
						
		# 				funding_round = funding_detail["series"]

		# 			else:
		# 				funding_round = "NULL"

		# 			# create an investment
		# 			investment = model.Investment(
		# 				investmentcompany_id=investmentcompany.id,
		# 				portfoliocompany_id=portfoliocompany.id,
		# 				money_raised=money_raised,
		# 				funding_round=funding_round)
		# 			# add it to the session
		# 			model.session.add(investment)

	model.session.commit()

		#use investmentcompany.id for when investmentcompany_id is in a column
		
def load_portfoliocompanies():
	

	##############  Instantiating Investment b/w Investment Company and Portfolio Company  ##############

	# use pc data drill down to data/relashionship/funding_rounds/items
	funding_rounds = pcompany_data[RELATIONSHIPS]["funding_rounds"][ITEMS]
	# iterate through items to get path to funding round
	for item in funding_rounds:

		funding_round_permalink = item["path"]
	
		# use path to request data on each funding round
		funding_detail = requests.get("http://api.crunchbase.com/v/2/"+funding_round_permalink+"?user_key="+str(CRUNCHBASE_API_KEY)).json()[DATA][PROPERTIES]
		# pull info to create an investment instance
		
		if "money_raised" in funding_detail:

			money_raised = funding_detail["money_raised"]

		if "series" in funding_detail:
			
			funding_round = funding_detail["series"]

		else:
			funding_round = "NULL"

		# create an investment
		investment = model.Investment(
			investmentcompany_id=investmentcompany.id,
			portfoliocompany_id=portfoliocompany.id,
			money_raised=money_raised,
			funding_round=funding_round)
		# add it to the session
		model.session.add(investment)
	
	##############  Instantiating Investment Company Partners ###############	
	
	# create parter instance with data available in investment company details
	for partner in icompany_data[RELATIONSHIPS]["current_team"][ITEMS]:
		
		partner = model.Partner(
			first_name=partner["first_name"],
			last_name=partner["last_name"],
			title=partner["title"],
			investmentcompany_id=investmentcompany.id)
		
		model.session.add(partner)
	

	##############  Instantiating Investment Company Sector Focuses ###############

	# create sector focus instance with data available in investment company details
	if "sectors" in icompany_data[PROPERTIES]:
		for sector in icompany_data[PROPERTIES]["sectors"]:
			# only want sector in the table once, so create a set just like portfolio companies
			if sector not in sectors_set:

				sector = model.SectorFocus(sector=sector)
				
				model.session.add(sectorfocus)

				sectors_set.add(sector)

	


model.session.commit()