from environ import Env
env = Env()

import yfinance as yf
import pandas as pd
import glob
from pathlib import Path
ROOT = Path(__file__).resolve(strict=True).parent.parent.parent.parent
APP = Path(__file__).resolve(strict=True).parent.parent
import os
import time

def yfinance_history(ticker, timeframe="10y", category=False, new=True):
    if not category:
        if new:
            try: os.mkdir(f'{ROOT}/data/{timeframe}')
            except: pass
            history = yf.Ticker(ticker).history(period=timeframe)
            time.sleep(float(env('YF_SLEEP')))
            history['Ticker'] = ticker
            history.dropna(inplace=True)
            history.to_csv(f"{ROOT}/data/{timeframe}/{ticker}.csv")
        else: 
            history = pd.read_csv(f"{ROOT}/data/{timeframe}/{ticker}.csv")
    elif category:
        if new:
            try: os.mkdir(f'{ROOT}/data/{category}')
            except: pass
            catg = eval(open(f'{APP}/data/tags/{category}.txt', "r").read())
            for ticker in catg:
                history = yf.Ticker(ticker).history(period=timeframe)
                time.sleep(float(env('YF_SLEEP')))
                history['Ticker'] = ticker
                history.dropna(inplace=True)
                history.to_csv(f'{ROOT}/data/{category}/{ticker}.csv')
        filepaths = glob.glob(f"{ROOT}/data/{category}/*.csv")
        history = pd.concat(map(pd.read_csv, filepaths))
        history.dropna(inplace=True)

    return history
