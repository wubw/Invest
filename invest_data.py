import pandas as pd
import os

stickers = ['D05.SI', '0700.HK','AAPL', '510310.SS' ]


def load_data():
    data = {}

    for s in stickers:
        file_path = os.path.join('data', s+'.csv')
        d = pd.read_csv(file_path)
        dt_idx = pd.DatetimeIndex(d['Date'])
        d.index = dt_idx
        data[s] = d

    return data
