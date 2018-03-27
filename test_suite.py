import pytest
from data import pull_data, get_risk_free_rate, calculate_returns
from portfolio import Portfolio
import pandas as pd

class TestDataClass(object):
    def test_stock_count(self):
        #Configuration
        stocks = ['IBB','FB','GOOGL','IYH','IBM','MMM']
        start_date = pd.to_datetime('2015-01-10')
        end_date = pd.to_datetime('2015-03-15')

        #Nested JSON
        results = pull_data(stocks, start_date, end_date) 

        assert len(results['stock_dict'].keys()) == len(stocks)
