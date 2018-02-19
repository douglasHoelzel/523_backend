from flask import Flask, jsonify, request
from flask_cors import CORS
from data_pull import *

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
    start_date = request.get_json()['start_date']
    end_date = request.get_json()['end_date']

    #Initial data pull
    stock_dict = pull_data(stocks, start_date, end_date)

    #Calculate log returns
    return_dict = calculate_returns(stock_dict)

    return jsonify(return_dict)
    
    #return jsonify(pull_data(stocks,start_date,end_date)) 
    

if __name__ == "__main__":
	app.run(debug=True, port=8080)