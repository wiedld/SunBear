from flask import Flask, render_template, redirect, request, jsonify
import model
import API
import os

app = Flask(__name__)
app.secret_key = os.environ["flask_app_key"]


@app.route("/")
def index():
    return render_template('landing.html')


# Creating routes for the front end to asynchronously call; can alter these as needed
@app.route("/get_zipcode_info")
def get_zipcode_info(zipcode_str):
	"""Will taker a zipcode parameter and return a JSON object to the caller for D3 to parse."""
	pass


@app.route("/get_county_info")
def get_county_info(county_name):
	pass


@app.route("/get_state_info")
def get_state_info(state_name):
	pass


@app.route("/get_country_info")
def get_country_info(country_name):
	pass


def main():
    pass



if __name__ == "__main__":
    main()
    # app.run(host="0.0.0.0", debug=False)
    app.run(debug=True)

