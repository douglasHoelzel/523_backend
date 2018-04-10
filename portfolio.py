import numpy as np
import pandas as pd
import scipy.optimize

class Portfolio(object):

    ####### Notes #######

    #Right now we're only concerned with monthly frequency
    #Need to explore new objective functions to optimize for
    #Need to find a volatility proxy that will work with shorter intervals
    
    def __init__(self, start_date, end_date, return_dict, interest_rates, frequency, transaction_costs): 
        self.number_assets = len(return_dict.keys()) #Stock symbols are the keys 
        self.start_date = start_date
        self.end_date = end_date
        self.return_dict = return_dict
        self.interest_rates = interest_rates
        self.assets = None
        self.initial_weights = np.ones(self.number_assets) / self.number_assets #Initialize to equal weight
        self.optimized_weights = {} #see optimize portfolio
        #self.prestart_return_dict = prestart_return_dict #Would be used in alternative volatility calculations
        self.dates = return_dict[next(iter(return_dict))].index #Potentially useful if we do daily values
        self.frequency = frequency
        self.rebalance_dates = None
        self.rebalance_date_returns = {} #see optimize portfolio
        self.calculate_rebalance_date() #Fill self.rebalance_dates
        self.calculate_assets() #Fills self.assets
        self.transaction_costs = transaction_costs # 0 or 1

    #Fill in rebalance dates
    def calculate_rebalance_date(self):
        if self.frequency == 'daily': #Handle daily case
            self.rebalance_dates = self.dates
        elif self.frequency == 'weekly': #Handle weekly case
            temp = self.return_dict[next(iter(self.return_dict))].resample('W').sum()
            self.rebalance_dates = temp.index
        elif self.frequency == 'monthly': #Handle monthly case
            temp = self.return_dict[next(iter(self.return_dict))].resample('M').sum().index[:-1]
            date_list = [self.return_dict[next(iter(self.return_dict))].index[0]]
            for t in temp:
                date_list.append(t)
            self.rebalance_dates = date_list

    #Build an n (dates) by m (log returns) portfolio for all assets
    def calculate_assets(self):
        temp_dict = {}
        for key in self.return_dict.keys():
            temp_dict[key] = self.return_dict[key]['Log Returns']
    
        self.assets = pd.DataFrame(temp_dict) 
            
    #Portfolio return (scalar)
    def calculate_total_return(self, weights, assets): 
        returns_vector = assets.dot(weights)
        return returns_vector.sum()

    #Portfolio return (vector)
    def calculate_vector_return(self, weights, assets): 
        return assets.dot(weights)

    #Measure of volatility, denominator of the sharpe_ratio   
    def sum_squared_differences(self, weights, assets):
        portfolio_return = self.calculate_vector_return(weights, assets) 
        portfolio_mean_return = portfolio_return.mean()
        sum_squared_differences = ((portfolio_return-portfolio_mean_return)**2).sum()

        return sum_squared_differences

    #Risk adjusted measurement of return
    def sharpe_ratio(self, weights, assets): 
        portfolio_return = self.calculate_vector_return(weights, assets)
        portfolio_return_minus_rf = portfolio_return - self.interest_rates["daily_rf_rate"]
        sharpe_ratio = portfolio_return_minus_rf.mean()/self.sum_squared_differences(weights, assets)

        return sharpe_ratio

    #Negates objective function, will add more objective functions in the future
    def objective_function(self, weights, assets):
        return (-1 * self.sharpe_ratio(weights, assets))

    def optimize_portfolio(self):
        
        #Constraints
        cons = {'type':'eq', 
                'fun': lambda x: np.sum(np.abs(x)) - 1}  #Weights must sum to one (absolute value)

        #Element bounds
        bounds = [(-1., 1.)] * len(self.initial_weights) #Shorts are allowed, no leverage
        
        
        date_len = len(self.rebalance_dates)
        for i in range(date_len):
            if date_len - i == 1:
                #This is the last value
                sliced_assets = self.assets.loc[self.rebalance_dates[i] : self.end_date]
            else:
                #Either the first or an inner value
                sliced_assets = self.assets.loc[self.rebalance_dates[i] : self.rebalance_dates[i+1]]
            
            #If transaction costs, subtract 2.5% from returns on rebalance date
            if int(self.transaction_costs) == 1:
                sliced_assets.iloc[0] = sliced_assets.iloc[0] - .025
                
            results = scipy.optimize.minimize(self.objective_function, self.initial_weights, args=(sliced_assets), 
                                                method= "SLSQP", constraints=cons, bounds=bounds, 
                                                options={'disp': True, #Turn off display in production
                                                         'maxiter': 1000})
            
            #Assign optimized weights
            weight_list = [float(weight) for weight in results.x] #decimal
            weights_pct = ["{0:.3f}%".format(weight * 100) for weight in results.x] #percent
            self.optimized_weights[self.rebalance_dates[i].strftime('%Y-%m-%d')] = list(zip(sliced_assets.columns,weight_list,weights_pct)) #stock symbol, decimal, percent
            
            #Assign return values
            self.rebalance_date_returns[self.rebalance_dates[i].strftime('%Y-%m-%d')] = float(self.calculate_total_return(results.x, sliced_assets))
        
        return {"optimized_weights": self.optimized_weights,
                "optimized_returns": self.rebalance_date_returns
                }




