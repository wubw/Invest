from datetime import datetime, timedelta


def get_price(df, time):
    dt = datetime.strptime(time, '%Y-%m-%d')
    idx = dt.strftime('%Y-%m-%d')

    cnt = 5
    while not idx in df.index:
        dt = dt + timedelta(days=1)
        idx = dt.strftime('%Y-%m-%d')
        cnt -= 1
        if cnt == 0:
            return None

    return df.loc[idx]['Adj Close']


def get_period_year(start_td, end_td):
    time_delta = end_td-start_td
    period_y = time_delta.days/365

    return period_y
