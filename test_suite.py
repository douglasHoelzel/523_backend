import pytest
from data import pull_data, get_risk_free_rate, calculate_returns
from portfolio import Portfolio
import pandas as pd

class TestDataClass(object):
    #Test to make sure we get same number of assets back from datapull
    def test_stock_count(self):
        #Configuration
        stocks = ['IBB','FB','GOOGL','IYH','IBM','MMM']
        start_date = pd.to_datetime('2015-01-10')
        end_date = pd.to_datetime('2015-03-15')

        #Nested JSON
        results = pull_data(stocks, start_date, end_date) 

        assert len(results['stock_dict'].keys()) == len(stocks) #length of stocks list should be the same in and out

    #Test to make sure we get the correct number of rows from data pull
    def test_data_length(self):
        #Configuration
        stocks = ['IBB','FB','GOOGL','IYH','IBM','MMM']
        start_date = pd.to_datetime('2018-01-01')
        end_date = pd.to_datetime('2018-01-31')

        #Nested JSON
        results = pull_data(stocks, start_date, end_date) 

        assert results['stock_dict']['IBB'].shape[0] == 21 #21 trading days in January 2018

    #Test to ensure correct risk free rate
    def test_dailyrf_rate(self):
        #Configuration
        start_date = pd.to_datetime('2018-01-01')
        end_date = pd.to_datetime('2018-01-31')

        #Nested JSON
        interest_rates = get_risk_free_rate(start_date,end_date)

        assert abs(interest_rates['daily_rf_rate'] - .0041) < .0001  #Known to be approximately .0041 for the month of January 2018