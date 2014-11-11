import model


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
	load_iqt_vc_partners()

	
if __name__ == "__main__":
	main()	