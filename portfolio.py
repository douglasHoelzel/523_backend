import numpy
import pandas

class portfolio(object):
    
    #Default constructor
    def __init__(self, return_dict, interest_rates, prestart_return_dict, frequency): #frequency can be daily, weekly, monthly
        self.tickers = return_dict.keys() #Stock symbols are the keys 
        self.return_dict = return_dict
        self.interest_rates = interest_rates
        self.portfolio = None
        self.weightings = None
        self.prestart_return_dict = prestart_return_dict #Used to calculate the first covariance value
        self.dates = return_dict[next(iter(return_dict))].index #Finds an arbitrary key, gets the datetime index from it
        self.all_dates = return_dict[next(iter(self.return_dict))].resample('D').sum() #Includes NAN dates
        self.frequency = frequency
        self.rebalance_dates = None
        self.rebalance_date_returns = None #empty for now, will be appended to later
        self.calculate_rebalance_date() #Calculate the rebalance dates depending on frequency
        self.calculate_portfolio() #Forms n * m matrix 

    #Fill in rebalance dates
    def calculate_rebalance_date(self):
        if self.frequency == 'daily': #Handle daily case
            self.rebalance_dates = self.dates
        elif self.frequency == 'weekly': #Handle weekly case
            temp = self.return_dict[next(iter(self.return_dict))].resample('W').sum()
            self.rebalance_dates = temp.index
        elif self.frequency == 'monthly': #Handle monthly case
            temp = self.return_dict[next(iter(self.return_dict))].resample('M').sum()
            self.rebalance_dates = temp.index

    def calculate_portfolio(self):
        #Compute n by m portfolio
        temp_dict = {}
        index = self.return_dict[next(iter(self.return_dict))].index
        for key in self.return_dict.keys():
            temp_dict[key] = self.return_dict[key]['Log Returns']
    
        self.portfolio = pd.DataFrame(temp_dict)
            
    #Portfolio return (scalar)
    def calculate_total_return(assets, weightings): 
        returns_vector = assets.dot(weightings)
        return returns_vector.sum()

    #Portfolio return (vector)
    def calculate_vector_return(): #matrix of assets (N [days] * M [assets]), vector of weightings (M*1)
        
        #Description
        #We take the two matracies, and multiple them together ((N*M)*(M*1))
        #This yields a vector (M*1) of daily returns for the portfolio

        #Output
        #A vector representing the return for the portfolio for each day over the period

    def calculate_st_dev(): #Weight vector (1*M), rebalancing frequency, cov-interval (4 weeks prior), return_dict (so that we can access log return for each asset) (ALREADY AVAILABLE VIA CONSTRUCTOR)
        
        #Description
        #w'Sw
        #Multiply the weight vector transpose by the S matrix and then again by the weight vector
        #See picture for outline of S
        #Take square root of resulting scalar

        #Output
        #Scalar representation of standard deviation

    def calculate_sharpe_ratio(weights): #Takes in a vector of weights 



    def optimize_portfolio():
        #INSERT CODE

