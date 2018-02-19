import quandl as q
import pandas as pd
import numpy as np

#Key to connect to the Quandl API
#TODO: configure api key as env variable in cloudapps
q.ApiConfig.api_key = "xaFxr9SP6Wd5sKFHdEax"

#Pull only adjusted closing price
def pull_data(stocks, start_date, end_date):
    #TODO: Add validation for stocks

    stock_dict = {}

    for stock in stocks:
        stock_data = q.get("EOD/{0}.11".format(stock), #Only pull closing price
				start_date="{0}".format(start_date), 
				end_date="{0}".format(end_date))
            
        stock_dict[stock] = stock_data 

    return stock_dict

#Log returns, takes in dict of pd dataframes
def calculate_returns(stock_dict):
    
    return_dict = {}
    for stock in stock_dict:
        #return_dict[stock] = np.log(1+stock_dict[stock]['Adj_Close'].pct_change().dropna())
        temp = np.log(1+stock_dict[stock]['Adj_Close'].pct_change().dropna())
        return_dict[stock] = temp.values.tolist()

    return return_dict

        

    

        

