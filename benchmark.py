import numpy as np
import pandas as pd

class Benchmark(object):

    def __init__(self, return_dict, benchmark):
        self.return_dict = return_dict #Dictionary
        self.benchmark = benchmark #String

    #Calculate the monthly returns and cumulative returns 
    def form_returns(self):
        monthly_ret = self.return_dict[self.benchmark[0]].resample('M').sum() #Monthly returns
        date_list = [date.strftime('%Y-%m-%d') for date in monthly_ret.index] #Dates of monthly returns

        #Returns for each date
        return_dict = dict(list(zip(date_list,monthly_ret['Log Returns'])))

        #Cumulative returns for each date
        cum_ret = monthly_ret['Log Returns'].cumsum()
        cumulative_return_dict = dict(list(zip(date_list, cum_ret)))
                
        return {"benchmark_monthly_returns": return_dict,
                "benchmark_cumulative_returns": cumulative_return_dict
                }
