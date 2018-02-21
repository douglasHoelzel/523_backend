import numpy
import pandas

class portfolio(object):
    
    #Default constructor
    def __init__(self, return_dict):
        self.tickers = return_dict.keys() #Stock symbols are the keys 
        self.return_dict = return_dict
        self.dates = return_dict[next(iter(return_dict))].index #Finds an arbitrary key, gets the datetime index from it

    def calculate_return():
        #INSERT CODE

    def calculate_return_range(start_date, end_date):
        #INSERT CODE

    def optimize_portfolio(objective_function, frequency, constraints):
        #INSERT CODE

