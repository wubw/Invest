import pandas as pd
import os

stickers = ['D05.SI', 'ME8U.SI', 'AJBU.SI',
            'C2PU.SI', 'BABA', 'MSFT', 'AAPL', 'NVDA', 'SPY', "ARKK"]


def load_data():
    data = {}

    for s in stickers:
        file_path = os.path.join('data', s+'.csv')
        d = pd.read_csv(file_path)
        dt_idx = pd.DatetimeIndex(d['Date'])
        d.index = dt_idx
        data[s] = d

    return data
