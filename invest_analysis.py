from datetime import datetime, timedelta
import pandas as pd

current_y = 2021


def get_price(df, time):
    dt = datetime.strptime(time, '%Y-%m-%d')
    idx = dt.strftime('%Y-%m-%d')

    while not idx in df.index:
        dt = dt + timedelta(days=1)
        idx = dt.strftime('%Y-%m-%d')

    return df.loc[idx]['Adj Close']


def passive_invest_stock(df, start_td, end_td, inv_interval, invest_strategy):
    cost_sum = 0
    unit_volum = 5
    next_time_td = None
    start_price = 0
    for index, row in df.iterrows():
        if index < start_td:
            continue
        if index > end_td:
            end_td = index
            break

        price = row['Adj Close']
        if cost_sum == 0:
            cost_sum += unit_volum*price
            next_time_td = index + timedelta(days=inv_interval)
            start_price = price
            start_td = index
            continue
        if index > next_time_td:
            unit_volum, cost_sum = invest_strategy(
                unit_volum, cost_sum, price, start_price)
            next_time_td += timedelta(days=inv_interval)

    return cost_sum, unit_volum, start_td, end_td


def return_analysis_stock(current_price, cost_sum, cost_volum, start_td, end_td):
    time_delta = end_td-start_td
    period_y = time_delta.days/365
    current_total_value = cost_volum*current_price
    price_increase = (current_total_value-cost_sum)/cost_sum
    annualized_return = ((1+price_increase)**(1/period_y))-1

    return annualized_return, period_y, price_increase


def calculate_stock(df, start_td, end_td, invest_strategy):
    cost_sum, unit_volum, start_td, end_td = passive_invest_stock(df,
                                                                  start_td, datetime.now(), 30.4, invest_strategy)

    current_price = df.iloc[-1:]['Adj Close'].values[0]
    annualized_return, period_y, price_increase = return_analysis_stock(
        current_price, cost_sum, unit_volum, start_td, end_td)

    return annualized_return, price_increase, current_price, cost_sum, unit_volum, start_td, period_y


def calculate_stocks(data, stickers, start_td, end_td, strategy):
    result_df = pd.DataFrame(
        columns=['Price inc', 'Ann ret', 'Start time', 'Inv period', 'Unit vol', 'Total inc'])
    for s in stickers:
        ar, price_increase, current_price, cost_sum, unit_volum, s_td, period_y = calculate_stock(
            data[s], start_td, end_td, strategy)
        series = pd.Series({'Price inc': price_increase, 'Ann ret': ar,
                            'Start time': s_td, 'Inv period': period_y, 'Unit vol': unit_volum, 'Total inc': current_price*unit_volum-cost_sum}, name=s)
        result_df = result_df.append(series)

    return result_df


def calculate_stocks_various_start_till_now(data, stickers, start_y, invest_strategy):
    start_time_arr = range(start_y, 2021)
    result = {}

    for y in start_time_arr:
        for s in stickers:
            start_td = datetime.strptime(str(y)+'-1-1', '%Y-%m-%d')
            ar, _, _, _, _, _, _ = calculate_stock(
                data[s], start_td, datetime.now(), invest_strategy)
            if s not in result:
                result[s] = {}
            result[s][str(y)] = ar

    start_time_arr = range(start_y, 2021)
    columns = []
    for y in start_time_arr:
        columns.append(str(y))
    result_df = pd.DataFrame(columns=columns)
    for s in stickers:
        series = pd.Series(result[s], name=s)
        result_df = result_df.append(series)

    return result_df


def calculate_stocks_various_period(data, stickers, start_y, period_y, invest_strategy):
    start_time_arr = range(start_y, 2021)
    for s in start_time_arr:
        result = calculate_stocks_annual_return(
            data, stickers, s, s+period_y, invest_strategy)