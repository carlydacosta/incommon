from flask import Flask, request, render_template
import os

# configuration
CRUNCHBASE_API_KEY = os.environ.get('CRUNCHBASE_API_KEY')
APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')

app = Flask(__name__)

app.secret_key = 'a4c96d59-57a8-11e4-8b97-80e6500ee2f9'

@app.route("/")
def index():
	#request from the API organizations with IQT as investor
	iqt_investments
	return render_template("index.html",
		iqt_investments=iqt_investments)


if __name__ == "__main__":
	app.run(debug=True)