from environ import Env
env = Env()

import numpy as np
import pandas as pd
from datetime import date

from earnalotbot.bot.utils.yfinance_history import *

from pathlib import Path
ROOT = Path(__file__).resolve(strict=True).parent.parent.parent.parent



# https://www.top1000funds.com/wp-content/uploads/2010/11/FAJskulls.pdf

def get_turbulence_index():
    turbulence_file_loc = f'{ROOT}/data/turbulence_index.csv'
    turbulence = pd.read_csv(turbulence_file_loc)
    return turbulence

def create_turbulence_index():

    today = date.today()
    today = today.strftime("%Y-%m-%d")
    try:
        df = yfinance_history(ticker=False, timeframe="10y", category='sp100', new=False)
        df = df[['Date', 'Ticker', 'Open', 'Close', 'High', 'Low', 'Volume']]
        df = df.sort_values(['Ticker', 'Date'], ignore_index=True)
        unique_dates = df.Date.unique()
        most_recent_date = df['Date'].max()
        most_recent_date = most_recent_date.strftime("%Y-%m-%d")
        assert(most_recent_date == today)
        # TODO: replace assert with a func to update data
    except:
        df = yfinance_history(ticker=False, timeframe="10y", category='sp100', new=True)
        df = df[['Date', 'Ticker', 'Open', 'Close', 'High', 'Low', 'Volume']]
        df = df.sort_values(['Ticker', 'Date'], ignore_index=True)
        unique_dates = df.Date.unique()

    one_year = 252
    turbulence_index = [0]*one_year
    skip_counter=0
    init_skips = 2
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pivot.html
    df = df.pivot(index='Date', columns='Ticker', values='Close').pct_change()
    for i in range(one_year, len(unique_dates)):

        before_today = (unique_dates[i] > df.index)
        after_one_year_ago = (df.index >= unique_dates[i - one_year])
        # https://stackoverflow.com/questions/10062954/valueerror-the-truth-value-of-an-array-with-more-than-one-element-is-ambiguous
        prev_year = df[before_today & after_one_year_ago].dropna(axis='columns')

        filtered_tickers = [x for x in prev_year]

        prev_year_mean = np.mean(prev_year, axis=0)
        today = df[df.index == unique_dates[i]]
        mean_variances = today[filtered_tickers] - prev_year_mean
        mean_variances = mean_variances.values # [[0.017 0.019 0.008]]
        mean_variances_transposed = mean_variances.T # [[0.017][0.019][0.008]]

        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.cov.html
        covariances = prev_year.cov()
        # https://numpy.org/doc/stable/reference/generated/numpy.linalg.pinv.html
        covariances_inversed = np.linalg.pinv(covariances) # [[9949.678...1367.860]...[1367.860...47611.480]]

        # https://numpy.org/doc/stable/reference/generated/numpy.dot.html
        score = mean_variances.dot(covariances_inversed).dot(mean_variances_transposed)

        if score > 0:
            skip_counter += 1
            if skip_counter > init_skips: turbulence_index.append(score[0][0])
            # avoid outliers in the beginning - they'll sckew the data dispraportionately later down the line
            else: turbulence_index.append(0)
        else: turbulence_index.append(0)
    
    
    df = pd.DataFrame({'date':df.index, 'turbulence':turbulence_index})
    df = df.iloc[int(one_year+init_skips+1):]
    df.to_csv(f'{ROOT}/data/turbulence_index.csv')
    print(df.tail(100))
    t = df['turbulence'].tolist()
    t.sort()
    t = t[25:-25]
    print(f'range: {t[0]} - {t[-1]}')
    print(f'average: {sum(t)/len(t)}')

