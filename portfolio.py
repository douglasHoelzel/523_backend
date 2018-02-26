import numpy
import pandas

class portfolio(object):
    
    #Default constructor
    def __init__(self, return_dict, prestart_return_dict, frequency): #frequency can be daily, weekly, monthly
        self.tickers = return_dict.keys() #Stock symbols are the keys 
        self.return_dict = return_dict
        self.prestart_return_dict = prestart_return_dict #Used to calculate the first covariance value
        self.dates = return_dict[next(iter(return_dict))].index #Finds an arbitrary key, gets the datetime index from it
        self.frequency = frequency
        self.rebalance_dates = None
        self.rebalance_date_returns = None #empty for now, will be appended to later
        self.fill_constructor() #Calculate the rebalence dates depending on frequency

    def fill_constructor():
        

    def calculate_total_return(): #matrix of assets (N [days] * M [assets]), vector of weightings (M*1)
        
        #Description
        #We take the two matracies, and multiple them together ((N*M)*(M*1))
        #This yields a vector (M*1) of daily returns for the portfolio
        #We can sum this vector to give a return over the period (whatever date is passed in by user)

        #Output
        #A scalar representing the return for the period

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

    def optimize_portfolio():
        #INSERT CODE

