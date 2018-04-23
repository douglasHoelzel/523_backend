# Project Title

This is the Python backend for my Computer Science 523 class (Software Engineering). The purpose of this application is to retrieve price information from Quandl on a set of financial assets, convert them to log returns, form a portfolio, and optimize that portfolio given a set of parameters. Overall, this code creates the necessary data for our frontend view

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

To install depenencies use "pip install -r requirements.txt" from the directory where the code is located. For a list of dependancies, check out requirements.txt 

### Layout

app.py = The entry point of the application. This is where all the routing is handled and calls to other modules are made. This is also the home of the flask server
benchmark.py = The object dedicated to forming and returning information about a user provided benchmark
portfolio.py = The object dedicated to forming and returning information about a set of user provided assets given a date range, rebalancing frequency, etc
data.py = The module used for data preprocessing needed in portfolio.py and benchmark.py
data_test_suite.py = All unit tests related to the data.py object
portfolio_test_suite.py = All unit tests related to the portfolio.py object
benchmark_test_suite.py = All unit tests related to the benchmark.py object


## Running the tests

Navigate to the directory containing any of the test suites. Then, for example, run "pytest portfolio_test_suite.py" and the unit tests should execute successfully

## Deployment

See the client handoff plan on our website for more details http://test-hoelzel.cloudapps.unc.edu/#!/home. The application is deployed on Carolina CloudApps under UNC Economics department credentials


## Contributing

Nicholas McHenry
Douglas Hoelzel
Avery Lue
Kurtis Bass

## Author

Nicholas McHenry

## Acknowledgments

Micheal Aguilar
