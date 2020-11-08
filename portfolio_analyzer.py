
from stock_analyzer import StockAnalyzer
from datetime import datetime, timedelta
import pandas as pd


class PortfolioAnalyzer:
    def __init__(self, data, invest_strategy):
        self.data = data
        self.invest_strategy = invest_strategy
        self.current_y = 2021

    def calculate(self, start_td, end_td):
        result_df = pd.DataFrame()
        for s in self.data.keys():
            #print('==================== ' + s + ' ====================')
            sa = StockAnalyzer(self.data[s], self.invest_strategy)
            ret = sa.calculate(start_td, end_td)
            series = pd.Series(ret, name=s)
            result_df = result_df.append(series)

        return result_df

    def calculate_with_period(self, start_y, period_y):
        start_time_arr = range(start_y, self.current_y)
        result = {}
        for y in start_time_arr:
            for s in self.data.keys():
                sa = StockAnalyzer(self.data[s], self.invest_strategy)
                start_td = datetime.strptime(str(y)+'-1-1', '%Y-%m-%d')
                end_td = datetime.strptime(str(y+period_y)+'-1-1', '%Y-%m-%d')
                ret = sa.calculate(start_td, end_td)
                if s not in result:
                    result[s] = {}
                result[s][str(y)] = ret['Ann ret']

        columns = []
        for y in start_time_arr:
            columns.append(str(y))
        result_df = pd.DataFrame(columns=columns)
        for s in self.data.keys():
            series = pd.Series(result[s], name=s)
            result_df = result_df.append(series)

        sum_result = {}
        for y in start_time_arr:
            val = result_df[str(y)].mean()
            sum_result[str(y)] = val
        series = pd.Series(sum_result, name='Sum')
        result_df = result_df.append(series)

        print(series.mean())
        return result_df

    def calculate_till_now(self, start_y):
        return self.calculate_with_period(start_y, self.current_y-start_y)

    def compare_results(self, ret2, ret1):
        total_inc_ratio = ret2['Gain ratio'].sum()/ret1['Gain ratio'].sum()-1
        unit_vol_ratio = ret2['Unit vol'].sum()/ret1['Unit vol'].sum()-1
        return total_inc_ratio, unit_vol_ratio
