from flask import Flask, jsonify, request
from flask_cors import CORS
from data import *
import pandas as pd

app = Flask(__name__)
CORS(app)

#Initial test method
@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World'

#Take in information from user:
#List of assets
#Start date
#End date
@app.route('/api/info', methods=['POST']) 
def parse_info():
    
    stocks = request.get_json()['assets']
    start_date = pd.to_datetime(request.get_json()['start_date']) #Datetime object
    end_date = pd.to_datetime(request.get_json()['end_date'])

    #Initial data pull
    stock_dict = pull_data(stocks, start_date, end_date)

    #Calculate log returns
    return_dict = calculate_returns(stock_dict)

    #return jsonify(return_dict)
    

if __name__ == "__main__":
	app.run(debug=True, port=8080)