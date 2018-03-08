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
    prestart_dict = {}

    #Calculate a new start date to get an extra month of data
    day = 1
    month = start_date.month - 1
    year = start_date.year
    new_start_date = pd.to_datetime(str(year)+'-'+str(month)+'-'+str(day))

    for stock in stocks:
        stock_data = q.get("EOD/{0}.11".format(stock), #Only pull closing price
				start_date="{0}".format(new_start_date), #Pull an extra month of data
				end_date="{0}".format(end_date))
        
        prestart_dict[stock] = stock_data.loc[new_start_date:start_date]
        stock_dict[stock] = stock_data.loc[start_date:end_date]

    return {'stock_dict':stock_dict, 
            'prestart_dict':prestart_dict
            }

#Proxied by the US 1 year treasury (beginning of the period)
def get_risk_free_rate(start_date,end_date):
    rf_rate = q.get("FRED/DTB1YR", start_date="{0}".format(start_date),end_date="{0}".format(end_date))["Value"].mean()
    daily_rf_rate = np.power((rf_rate + 1), 1.0/252) - 1 #deannualize rf rate

    return {"rf_rate": rf_rate,
            "daily_rf_rate": daily_rf_rate
            }

#Log returns, appends to the stock_dict with a new return column
def calculate_returns(stock_dict):
    
    #return_dict = {}
    for stock in stock_dict:
        temp = np.log(1+stock_dict[stock]['Adj_Close'].pct_change())
        temp = temp.rename('Log Returns')
        stock_dict[stock] = stock_dict[stock].join(temp).dropna()
        #return_dict[stock] = temp.values.tolist() #Change back to pd dataframe

    return stock_dict #return_dict

        

    

        

