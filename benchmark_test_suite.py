import pytest
from data import pull_data, get_risk_free_rate, calculate_returns
from benchmark import Benchmark
import pandas as pd

#setup for tests

@pytest.fixture
def initialize_benchmark_variables():
    pytest.start_date = pd.to_datetime('2018-01-01')
    pytest.end_date = pd.to_datetime('2018-01-31')
    pytest.benchmarkString = "IVV"

@pytest.fixture
def initialize_benchmark(initialize_benchmark_variables):
    pytest.benchmark_results = pull_data(pytest.benchmarkString, pytest.start_date, pytest.end_date)
    pytest.benchmark_return_dict = calculate_returns(pytest.benchmark_results['stock_dict'])
    pytest.testBenchmark = Benchmark(pytest.benchmark_return_dict, pytest.benchmarkString)


#tests
class TestBenchmarkClass(object):

    #test initialize benchmark variables
    def test_benchmark_init_vars(self, initialize_benchmark_variables):
        
        assert pytest.benchmarkString == "IVV"
        assert pytest.start_date != 0
        assert pytest.end_date != 0

    #test initialize benchmark
    def test_benchmark_init(self, initialize_benchmark):
        testReturn = pytest.testBenchmark.return_dict
        testString = pytest.testBenchmark.benchmark

        assert testString == "IVV"
        assert (len(testReturn["I"])) == 20 #21 trading days in january, should have 20 returns

    def test_form_returns(self, initialize_benchmark):
        testOutput = pytest.testBenchmark.form_returns()
        testMonthly = testOutput["benchmark_monthly_returns"]
        testCumulative = testOutput["benchmark_cumulative_returns"]

        assert len(testOutput) == 2
        assert testMonthly == testCumulative #Only tested one month, so should be same
        assert testMonthly["2018-01-31"] < 0  #expected loss
        assert (testMonthly["2018-01-31"] + .2588) < .00001 #result of approximately .2588 expected



    


