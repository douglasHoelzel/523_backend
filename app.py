from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from data import pull_data, get_risk_free_rate, calculate_returns
from portfolio import Portfolio
from benchmark import Benchmark
import pandas as pd
import re

app = Flask(__name__)
CORS(app)

#Test to ensure active
@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World'

@app.route('/api/info', methods=['POST']) 
def parse_info():   

    #check date is valid format
    pattern = re.compile("^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$")
    if not pattern.fullmatch(request.get_json()['start_date']):
        abort(400)
    if not pattern.fullmatch(request.get_json()['end_date']):
        abort(400)

    stocks = request.get_json()['assets']
    benchmark = request.get_json()['benchmark'] #Needs to be a list
    start_date = pd.to_datetime(request.get_json()['start_date']) #Datetime object
    end_date = pd.to_datetime(request.get_json()['end_date'])
    frequency = request.get_json()['frequency']
    transaction_costs = request.get_json()['transaction_costs'] #0 or 1

    #is date valid range?  
    #Error code 1
    if start_date >= end_date:
        return jsonify({
            "Error_Code" : "1",
            "Error_Description" : "Inverted Date Range"
        })

    #Used for date interval checking
    date_diff = end_date - start_date
        
    #Error code 2
    if frequency == "monthly" and date_diff.days > 731: #2 years worth of days
        return jsonify({
            "Error_Code" : "2",
            "Error_Description" : "Too long of a date range (monthly). Please enter a range interval between 4 months and 2 years"
        })

    #Error code 3
    if frequency == "quarterly" and date_diff.days > 1461: #4 years worth of days
        return jsonify({
            "Error_Code" : "3",
            "Error_Description" : "Too long of a date range (quarterly). Please enter a range interval between 1 year and 4 years"
        })

    #Error code 4
    if frequency == "biannual" and date_diff.days > 2922: #4 years worth of days
        return jsonify({
            "Error_Code" : "4",
            "Error_Description" : "Too long of a date range (biannual). Please enter a range interval between 2 year and 8 years"
        })  

    #Error code 5
    if frequency == "monthly" and date_diff.days < 120: #4 months worth of days
        return jsonify({
            "Error_Code" : "5",
            "Error_Description" : "Too short of a date range (monthly). Please enter a range interval between 4 months and 2 years"
        })     

    #Error code 6
    if frequency == "quarterly" and date_diff.days < 365: #1 year worth of days
        return jsonify({
            "Error_Code" : "6",
            "Error_Description" : "Too short of a date range (quarterly). Please enter a range interval between 1 year and 4 years"
        })  

    #Error code 7
    if frequency == "biannual" and date_diff.days < 731: #2 years worth of days
        return jsonify({
            "Error_Code" : "7",
            "Error_Description" : "Too short of a date range (biannual). Please enter a range interval between 2 year and 8 years"
        })          

    #check if is string, make list if string
    if isinstance(benchmark, str):
        benchmark = [benchmark]

    #ensure stocks is list
    if not isinstance(stocks, list) :
        abort(400)

    #Initial data pull
    results = pull_data(stocks, start_date, end_date) 
    benchmark_results = pull_data(benchmark, start_date, end_date)

    #Get daily and annual risk free rate
    interest_rates = get_risk_free_rate(start_date,end_date)

    #Calculate log returns
    return_dict = calculate_returns(results['stock_dict'])
    benchmark_return_dict = calculate_returns(benchmark_results['stock_dict'])

    #Output for the portfolio
    portfolio = Portfolio(start_date, end_date, return_dict, interest_rates, frequency, transaction_costs)
    output = portfolio.optimize_portfolio()

    #Output for the benchmark
    benchmark = Benchmark(benchmark_return_dict,benchmark)
    benchmark_output = benchmark.form_returns()

    #Find matching keys, build joint data structure
    common_keys = set(output['cumulative_returns']).intersection(benchmark_output["benchmark_cumulative_returns"])
    intersect_dict = {}
    for key in common_keys:
        intersect_dict[key] = [output['cumulative_returns'][key],benchmark_output["benchmark_cumulative_returns"][key]]

    return jsonify({"optimized_cumulative_returns": output['cumulative_returns'],
                   "optimized_weights": output['optimized_weights'],
                   "benchmark_portfolio_intersection": intersect_dict,
                   "benchmark_cumulative_returns": benchmark_output['benchmark_cumulative_returns']
                     })
    

#For testing
#if __name__ == "__main__":
#	app.run(debug=True, port=8080)

#For Production
if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=8080)