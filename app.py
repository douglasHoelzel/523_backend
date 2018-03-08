from flask import Flask, jsonify, request
from flask_cors import CORS
from data import pull_data, get_risk_free_rate, calculate_returns
from portfolio import Portfolio
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
    frequency = request.get_json()['frequency']

    #Initial data pull
    results = pull_data(stocks, start_date, end_date) 

    #Get daily and annual risk free rate
    interest_rates = get_risk_free_rate(start_date,end_date)

    #Calculate log returns
    return_dict = calculate_returns(results['stock_dict'])
    prestart_return_dict = calculate_returns(results['prestart_dict'])

    portfolio = Portfolio(start_date, end_date, return_dict, interest_rates, prestart_return_dict, frequency)
    output = portfolio.optimize_portfolio()

    #BELOW THIS LINE IS USED FOR TESTING ON LOCALHOST

    return jsonify({"optimized_returns": output['optimized_returns'],
                   "optimized_weights": output['optimized_weights']  
                     })
    

#For testing
#if __name__ == "__main__":
#	app.run(debug=True, port=8080)

#For Production
if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=8080)