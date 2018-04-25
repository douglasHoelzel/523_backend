import pytest
from data import pull_data, get_risk_free_rate, calculate_returns
from portfolio import Portfolio
import pandas as pd

#Think about using fixtures to setup configuration

@pytest.fixture
def initialize_variables():
    pytest.stocks = ['IBB','FB','GOOGL','IYH','IBM','MMM']
    pytest.start_date = pd.to_datetime('2018-01-01')
    pytest.end_date = pd.to_datetime('2018-01-31')
    pytest.frequency = 'monthly'
    pytest.transaction_costs = 0

@pytest.fixture
def initialize_pull_variables():
    pytest.stocks = ['IBB','FB','GOOGL','IYH','IBM','MMM']
    pytest.start_date = pd.to_datetime('2018-01-01')
    pytest.end_date = pd.to_datetime('2018-04-01')

@pytest.fixture
def initialize_returns_variables():
    pytest.stocks = ['IBB','FB','GOOGL','IYH','IBM','MMM']
    pytest.start_date = pd.to_datetime('2018-01-01')
    pytest.end_date = pd.to_datetime('2018-01-05')
    pytest.frequency = 'monthly'
    pytest.transaction_costs = 0

@pytest.fixture
def initialize_simple_variables():
    pytest.stocks = ['FB', 'GOOG']
    pytest.start_date = pd.to_datetime('2018-01-01')
    pytest.end_date = pd.to_datetime('2018-01-04')
    pytest.frequency = 'monthly'
    pytest.transaction_costs = 0

@pytest.fixture
def init_simple_pull(initialize_simple_variables):
    pytest.stock_dict = pull_data(pytest.stocks, pytest.start_date, pytest.end_date)

@pytest.fixture
def initialize_simple_portfolio(initialize_simple_variables, init_simple_pull):
    pytest.return_dict = calculate_returns(pytest.stock_dict['stock_dict'])
    pytest.interest_rates = get_risk_free_rate(pytest.start_date,pytest.end_date)
    pytest.testPortfolio = Portfolio(pytest.start_date, pytest.end_date, pytest.return_dict, pytest.interest_rates, pytest.frequency, pytest.transaction_costs)
    return pytest.testPortfolio

@pytest.fixture
def init_pull(initialize_variables):
    pytest.stock_dict = pull_data(pytest.stocks, pytest.start_date, pytest.end_date)

@pytest.fixture
def init_returns_pull(initialize_returns_variables):
    pytest.stock_dict = pull_data(pytest.stocks, pytest.start_date, pytest.end_date)

@pytest.fixture
def initialize_portfolio(initialize_variables, init_pull):
    pytest.return_dict = calculate_returns(pytest.stock_dict['stock_dict'])
    pytest.interest_rates = get_risk_free_rate(pytest.start_date,pytest.end_date)
    pytest.testPortfolio = Portfolio(pytest.start_date, pytest.end_date, pytest.return_dict, pytest.interest_rates, pytest.frequency, pytest.transaction_costs)
    return pytest.testPortfolio

@pytest.fixture
def initialize_returns_portfolio(initialize_returns_variables, init_returns_pull):
    pytest.return_dict = calculate_returns(pytest.stock_dict['stock_dict'])
    pytest.interest_rates = get_risk_free_rate(pytest.start_date,pytest.end_date)
    pytest.testPortfolio = Portfolio(pytest.start_date, pytest.end_date, pytest.return_dict, pytest.interest_rates, pytest.frequency, pytest.transaction_costs)
    return pytest.testPortfolio



class TestDataClass(object):
    #Test to make sure we get same number of assets back from datapull
    def test_stock_count(self, initialize_pull_variables):
        #Configuration
        stocks = pytest.stocks
        start_date = pytest.start_date
        end_date = pytest.end_date

        #Nested JSON
        results = pull_data(stocks, start_date, end_date) 

        assert len(results['stock_dict'].keys()) == len(stocks) #length of stocks list should be the same in and out

    #Test to make sure we get the correct number of rows from data pull
    def test_data_length(self, initialize_pull_variables):
        #Configuration
        stocks = pytest.stocks
        start_date = pytest.start_date
        end_date = pytest.end_date


        #Nested JSON
        results = pull_data(stocks, start_date, end_date) 
        print(len(results))

        assert results['stock_dict']['IBB'].shape[0] == 61 #61 trading days in January to April 2018

    #Test to ensure correct risk free rate
    def test_dailyrf_rate(self, initialize_variables):
        #Configuration
        start_date = pytest.start_date
        end_date = pytest.end_date

        #Nested JSON
        interest_rates = get_risk_free_rate(start_date,end_date)

        assert abs(interest_rates['daily_rf_rate'] - .0041) < .0001  #Known to be approximately .0041 for the month of January 2018
    #Test to ensure that we are calculating log returns correctly
    def test_calculate_return(self):
        #Configuration
        price_list = [10,11]
        test_df = pd.DataFrame(price_list,columns=['Adj_Close']) #Test values
        test_dict = {'FB':test_df}

        #Nested JSON
        results = calculate_returns(test_dict)

        assert (results['FB']['Log Returns'].iloc[0] - .0953) < .0001 #Log percent change between 10 and 11 is approx 9.53%

class TestPortfolioClass(object):

    #First I want to test that the data is being entered in Portfolio correctly
    def test_Portfolio_init(self, initialize_portfolio):
        assert pytest.testPortfolio.number_assets == 6
        assert len(pytest.testPortfolio.interest_rates) > 0
        assert len(pytest.testPortfolio.dates) == 20
        assert pytest.testPortfolio.frequency == 'monthly'
        assert pytest.testPortfolio.transaction_costs == 0
        assert len(pytest.testPortfolio.assets) == len(pytest.testPortfolio.dates)
        assert len(pytest.testPortfolio.rebalance_dates) == 1



    #Practice test, testing to verify the correct amount of rebalance dates are being returned.
    def test_calc_rebalance_date_response_length(self, initialize_portfolio):


        pytest.testPortfolio.calculate_rebalance_date()

        assert len(pytest.testPortfolio.rebalance_dates) == 1 #expected amount of monthly rebalance dates given 1 month

   # TO BE ADDED:
   # def test_calc_rebalance_date(self, initialize_portfolio):

    def test_portfolio_dates(self, initialize_portfolio):
        assert len(pytest.testPortfolio.dates) == 20 #1 less than trading days

    def test_portfolio_dates_2(self, initialize_returns_portfolio):
        assert len(pytest.testPortfolio.dates) == 3 #same as previous, testing different data length
        
    #test assets in calculate_assets are same as those initialized in portfolio
    def test_width_calculate_assets(self, initialize_portfolio):

        pytest.testPortfolio.calculate_assets()

        #Number of assets should still be 6

        assert pytest.testPortfolio.number_assets == 6

    #test there are as many rows in assets as there are trading days in the portfolio
    def test_length_calculate_assets(self, initialize_portfolio):

        pytest.testPortfolio.calculate_assets()

        #Number of rows in assets matrix should be same as dates
        assert len(pytest.testPortfolio.assets) == 20

    #test that the total items in assets are the multiplication of those numbers
    def test_calculate_assets(self, initialize_portfolio):

        pytest.testPortfolio.calculate_assets()
        #number of assets should be the multiplication of those numbers
        assert pytest.testPortfolio.number_assets * len(pytest.testPortfolio.assets) == 120 #20 returns times 6 assets should make 120 data entries in assets

    #test accuracy of calculate_total_return
    def test_calculate_total_return(self, initialize_returns_portfolio):

        pytest.testPortfolio.calculate_assets()
        tempResult = pytest.testPortfolio.calculate_total_return(pytest.testPortfolio.initial_weights, pytest.testPortfolio.assets)

        assert .0265 < tempResult and tempResult < .0266 #calculated to .0266 rounding up, should be in this range

    #test accuracy of calculate_vector_return
    def test_calculate_vector_return(self, initialize_returns_portfolio):

        tempResult = pytest.testPortfolio.calculate_vector_return(pytest.testPortfolio.initial_weights, pytest.testPortfolio.assets)


        assert (tempResult[0] - .0425) < .0001 #.0425 is the result of multiplying the weight by the first return

    # #test sum_squared_differences
    def test_sum_squared_differences(self, initialize_returns_portfolio):
        
        
        tempResult = pytest.testPortfolio.sum_squared_differences(pytest.testPortfolio.initial_weights, pytest.testPortfolio.assets)

        assert tempResult - .000048 < .000001

    #test accuracy of sharpe_ratio function
    def test_sharpe_ratio(self, initialize_returns_portfolio):

        tempResult = pytest.testPortfolio.sharpe_ratio(pytest.testPortfolio.initial_weights, pytest.testPortfolio.assets)

        var1 = pytest.testPortfolio.calculate_vector_return(pytest.testPortfolio.initial_weights, pytest.testPortfolio.assets)
        var2 = var1 - pytest.testPortfolio.interest_rates["daily_rf_rate"]
        var3 = var2.mean()
        var4 = pytest.testPortfolio.sum_squared_differences(pytest.testPortfolio.initial_weights, pytest.testPortfolio.assets)

        expectedResult = var3 / var4
        assert expectedResult == tempResult


    #OPTIONAL FOR LATER
    # def test_sharpe_ratio_simple(self, initialize_simple_portfolio):

    #     tempResult = pytest.testPortfolio.sharpe_ratio(pytest.testPortfolio.initial_weights, pytest.testPortfolio.assets)
    #     assert 0

    # #test accuracy of objective_function


    def test_objective_function(self, initialize_returns_portfolio):
        var1 = pytest.testPortfolio.sharpe_ratio(pytest.testPortfolio.initial_weights, pytest.testPortfolio.assets)
        var1 = var1 * -1
        tempResult = pytest.testPortfolio.objective_function(pytest.testPortfolio.initial_weights, pytest.testPortfolio.assets)

        assert var1 == tempResult

