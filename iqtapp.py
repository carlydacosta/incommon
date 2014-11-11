from flask import Flask, render_template
import os, requests


# configuration
CRUNCHBASE_API_KEY = os.environ.get('CRUNCHBASE_API_KEY')
APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')



app = Flask(__name__)

@app.route("/", METHOD="GET")
def select_vc_pairs():
	# recieve two vc names
	# query for each vc and their investment portfolio
	# return common investments
	pass
	


if __name__ == "__main__":
	app.run(debug=True)

