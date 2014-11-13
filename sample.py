import memcache, requests, os

DATA="data"
ITEMS="items"


class CompareVcs():

	def __init__(self, vc1_path, vc2_path):
		if vc1_path == vc2_path:
			raise Exception("Firms must be different to compare.")
		self.vc1 = VC(vc1_path)
		self.vc2 = VC(vc2_path)
		
	def compare_investments(self):
		# go ahead and get the data of the company and add it to memcache
		self.vc1.get_data()
		self.vc2.get_data()

		i_1 = self.vc1.get_investments()
		i_2 = self.vc2.get_investments()

		common_investments_list = (set(item['invested_in']['name'] for item in i_1[ITEMS]) & set(item['invested_in']['name'] for item in i_2[ITEMS]))
		print "Investments in common: ", common_investments_list

		common_paths_list = (set(item['invested_in']['path'] for item in i_1[ITEMS]) & set(item['invested_in']['path'] for item in i_2[ITEMS]))
		print "common paths: ", common_paths_list

		pc_data_dict = {} # {pc path : pc data}

		for pc_path in common_paths_list:
			pc_path = pc_path.replace("organization/", "").encode("utf8")
			print pc_path
			pc_object = PortfolioCompany(pc_path)
			pc_data_dict[pc_path] = pc_object.get_data()
			
		print "PC dictionary complete."

		
		return common_investments_list



class VC():

	def __init__(self, vc_path):
		if vc_path is None:
			raise Exception("No VC path received to instantiate VC instance.")
		self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)
		self.vc_path = vc_path
		# self.all_vcs_key = "all_vc"
		self.vc_data_key = "data-%s" % vc_path
		self.vc_investments_key = "investments-%s" % vc_path

	def get_data(self):
		print "Made it to VC data"

		cache = self.mc.get(self.vc_data_key)
		if cache is not None:
			return cache

		c = Crunchbase()

		data = c.get_vc_data(self.vc_path)
		self.mc.set(self.vc_data_key, data)
		return data 

	def get_investments(self):
		print "Made it to VC investments"

		cache = self.mc.get(self.vc_investments_key)
		if cache is not None:
			return cache

		c = Crunchbase()

		data = c.get_vc_portfolio(self.vc_path)
		self.mc.set(self.vc_investments_key, data)
		#seed.load_investment_company(data)
		
		return data



class PortfolioCompany():

	def __init__(self, pc_path):
		if pc_path is None:
			print "No PC path received to instantiate PC instance."
		self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)
		self.pc_path = pc_path
		self.pc_data_key = "data-%s" % pc_path
		
	def get_data(self):
		print "Made it to PC data"

		cache = self.mc.get(self.pc_data_key)
		if cache is not None:
			return cache

		c = Crunchbase()

		data = c.get_pc_data(self.pc_path)
		self.mc.set(self.pc_data_key, data)
		return data



def save_vc_list():
	URL_BASE = "http://api.crunchbase.com/v/2/"
	API_KEY = os.environ.get('CRUNCHBASE_API_KEY')
	mc = memcache.Client(['127.0.0.1:11211'], debug=0)	
	c = Crunchbase()

	data = c.get_vc_list()

	number_of_pages = data['paging']['number_of_pages']

	for page in range(1, number_of_pages+1):
		print page
		cache_key = "vc_list_"+str(page)
		cache = mc.get(cache_key)
		
		if cache is not None:
			print "Returned page " + str(page) + " from cache."

		else:
			print "Not in cache.  Making API call..."
			response = requests.get(URL_BASE + "organizations?organization_types=investor&user_key=" + API_KEY + "&page=" + str(page))
			data = response.json()[DATA]
		
			if response.status_code is not 200:
				print "Failed lookup: %d" % response.status_code
				return None
			
			print "Setting page " + str(page) + " in cache."
			cache = mc.set(cache_key, data)



class Crunchbase():
	URL_BASE = "http://api.crunchbase.com/v/2/"
	def __init__(self):
		self.API_KEY = os.environ.get('CRUNCHBASE_API_KEY')
		self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)
		# this.API_SECRET_KEY = os.environ.get('APP_SECRET_KEY')


	def get_vc_list(self):
		#send request for vcs only to get the number of pages (this will include page 1 but we will just redo the request specifically by page #)
		print "Queried Crunchbase"
		response = requests.get(self.URL_BASE + "organizations?organization_types=investor&user_key=" + self.API_KEY)
		return response.json()[DATA]
		
	def get_vc_data(self, vc_path):
		return self._query(vc_path, "")
		
	def get_vc_portfolio(self, vc_path):
		return self._query(vc_path, "/investments")	

	def get_pc_data(self, pc_path):
		return self._query(pc_path, "")

	def _query(self, vc_path, target=""):
		print "Queried Crunchbase"
		response = requests.get(self.URL_BASE + "organization/" + vc_path + target + "?user_key=" + self.API_KEY)

		if response.status_code is not 200:
			print "Failed lookup: %d" % response.status_code
			return None
		return response.json()[DATA]



# def iqt_vc_partners_list():
	
# 	f = open("iqt_partners.csv")
# 	vc_partner_list = f.strip().split('/r')

# 	return vc_partner_list

def main():
	# vc = CompareVcs('sutter-hill-ventures', 'in-q-tel')
	# vc.compare_investments()
	# c = Crunchbase()
	# c.get_vc_list()
	save_vc_list()

	

if __name__ == "__main__":
	main()				
