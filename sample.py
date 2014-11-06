import requests

def main():
	
	#get a list of investor companies from CB
	#for each company, get a list of their portfolio companies

	sutter_hill_info = requests.get("http://api.crunchbase.com/v/2/organization/sutter-hill-ventures/investments?user_key=f0e2f7c3fd87b6dc6bc38c5ec8e7baf7")

	iqt_info = requests.get("http://api.crunchbase.com/v/2/organization/in-q-tel/investments?user_key=f0e2f7c3fd87b6dc6bc38c5ec8e7baf7")

	# The response is json object
	# Turn into a dictionary with .json()
	iqt_dict = iqt_info.json()
	sutter_hill_dict = sutter_hill_info.json()

	# Traverse through the dictionary to where the list of investment items are
	list_of_iqt_investment_items = iqt_dict["data"]["items"]
	list_of_sutter_investment_items = sutter_hill_dict["data"]["items"]
	
	# Iterate through each list, drilling down to the portfolio company name and appending the name to the appropriate list of portfolio companies.
	# portfolio_companies = {"in-q-tel": [], "sutter_hill": []}
	iqt_portfolio_companies = {"name": [item["invested_in"]["name"] for item in list_of_iqt_investment_items]}			
	sutter_portfolio_companies = {"name": [item["invested_in"]["name"] for item in list_of_sutter_investment_items]}
	common_investments = [item for item in set(iqt_portfolio_companies["name"]) & set(sutter_portfolio_companies["name"])]  ## THIS IS AN AMAZING TIME SAVER!!!
	# for item in common_investments:
	# 	print item
				

	# for item in list_of_iqt_investment_items:
	# 	portfolio_company_name = item["invested_in"]["name"]
	# 	iqt_portfolio_companies["name"].append(portfolio_company_name)
		# portfolio_companies["in-q-tel"].append(portfolio_company_name)

	# for item in list_of_sutter_investment_items:
	# 	portfolio_company_name = item["invested_in"]["name"]
	# 	sutter_portfolio_companies["name"].append(portfolio_company_name)
		# portfolio_companies["sutter_hill"].append(portfolio_company_name)

	# for portfolio_company in iqt_portfolio_companies["name"]:
	# 		if portfolio_company in sutter_portfolio_companies["name"]:
	# 			if portfolio_company not in common_investments["name"]:
	# 				common_investments["name"].append(portfolio_company)
			
	return common_investments



if __name__ == "__main__":
	main()