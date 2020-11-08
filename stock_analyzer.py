from datetime import datetime, timedelta
import pandas as pd
from common import get_price


class StockAnalyzer:
    def __init__(self, df, invest_strategy):
        self.df = df
        self.invest_strategy = invest_strategy

    def start_passive_invest(self, start_td, end_td, inv_interval):
        cost_sum = 0
        unit_volum = 1
        next_time_td = None
        start_price = 0
        e_td = end_td
        s_td = start_td
        for index, row in self.df.iterrows():
            if index < start_td:
                continue
            if index > end_td:
                break

            e_td = index
            price = row['Adj Close']
            if cost_sum == 0:
                s_td = index
                cost_sum += unit_volum*price
                next_time_td = index + timedelta(days=inv_interval)
                start_price = price
                start_td = index
                continue
            if index > next_time_td:
                inc_volum = self.invest_strategy(
                    price, start_price, self.df, index)
                unit_volum += inc_volum
                cost_sum += price*inc_volum
                next_time_td += timedelta(days=inv_interval)

        return cost_sum, unit_volum, s_td, e_td

    def calculate(self, start_td, end_td):
        cost_sum, unit_volum, start_td, end_td = self.start_passive_invest(
            start_td, end_td, 30.4)

        if cost_sum == 0 or start_td == end_td:
            return {'Gain ratio': 0, 'Ann ret': 0,
                    'Start time': start_td, 'Inv period': 0,
                    'Unit vol': 0}

        current_price = get_price(self.df, end_td.strftime('%Y-%m-%d'))
        time_delta = end_td-start_td
        period_y = time_delta.days/365
        current_total_value = unit_volum*current_price
        gain_ratio = (current_total_value-cost_sum)/cost_sum
        annualized_return = ((1+gain_ratio)**(1/period_y))-1

        return {'Gain ratio': gain_ratio, 'Ann ret': annualized_return,
                'Start time': start_td, 'Inv period': period_y,
                'Unit vol': unit_volum}
