import pandas as pd
from pandas_datareader import data as wb
import os

stickers = ['D05.SI', 'ME8U.SI', 'AJBU.SI', 'M44U.SI', 'C2PU.SI', 'C38U.SI', 'J69U.SI',
            '0700.HK','9988.HK', '9618.HK', '1299.HK', '2318.HK', '1398.HK', '3988.HK',
            'BABA', 'CQQQ', 'EDU',
            'GOOG', 'AAPL', 'MSFT', 'META', 'AMZN', 'SPY', 'QQQ', 'XLV', 'SOXX', 'NVDA',
            'PYPL', 'TSLA', 'U', 'ARKK', 'ARKW', 'ARKG', 'ARKQ', 'ARKF', 'PRNT', 
            '510310.SS' ]

all_price_cache = {}

def fetch_price(s):
    d = wb.DataReader(s, data_source='yahoo', start='1997-1-1')
    file_path = os.path.join('data', s+'.csv')
    d.to_csv(file_path)
    
    _ = all_price_cache.pop(s, None)

def fetch_all_price():
    for s in stickers:
        print(s)
        fetch_price(s)

def get_price(s):
    if s not in all_price_cache:
        file_path = os.path.join('data', s+'.csv')
        d = pd.read_csv(file_path)
        dt_idx = pd.DatetimeIndex(d['Date'])
        d.index = dt_idx
        all_price_cache[s] = d

    return all_price_cache[s]

def get_ledger():
    file_path =  os.path.join('data', 'ledger.csv')
    d = pd.read_csv(file_path)
    return d
