import time

from datetime import datetime, timedelta

from environ import Env

import robin_stocks.robinhood as rh

env = Env()
market_hours = rh.markets.get_market_today_hours("XNYS")
time.sleep(float(env('RH_SLEEP')))

def get_start_time(start_n_mins_before_open=5):
    try:
        start = datetime.strptime(market_hours['opens_at'], '%Y-%m-%dT%H:%M:%SZ')
        start -= timedelta(hours=5, minutes=start_n_mins_before_open)
        stop = datetime.strptime(market_hours['opens_at'], '%Y-%m-%dT%H:%M:%SZ')
        stop -= timedelta(hours=5)
        in_range = bool(start < datetime.now() < stop)
        return bool(market_hours['is_open'] and in_range)
    except:
        return False

def get_buy_time(start_n_mins_after_open=59, stop_n_mins_before_close=59):
    try:
        start = datetime.strptime(market_hours['opens_at'], '%Y-%m-%dT%H:%M:%SZ')
        start -= timedelta(hours=5, minutes=start_n_mins_after_open)
        stop = datetime.strptime(market_hours['closes_at'], '%Y-%m-%dT%H:%M:%SZ')
        stop -= timedelta(hours=5, minutes=stop_n_mins_before_close)
        in_range = bool(start < datetime.now() < stop)
        return bool(market_hours['is_open'] and in_range)
    except:
        return False

def get_hold_time(start_n_mins_before_close=59, stop_n_mins_before_close=3):
    try:
        start = datetime.strptime(market_hours['closes_at'], '%Y-%m-%dT%H:%M:%SZ')
        start -= timedelta(hours=5, minutes=start_n_mins_before_close)
        stop = datetime.strptime(market_hours['closes_at'], '%Y-%m-%dT%H:%M:%SZ')
        stop -= timedelta(hours=5, minutes=stop_n_mins_before_close)
        in_range = bool(start < datetime.now() < stop)
        return bool(market_hours['is_open'] and in_range)
    except:
        return False

def get_sell_time(start_n_mins_before_close=3):
    try:
        start = datetime.strptime(market_hours['closes_at'], '%Y-%m-%dT%H:%M:%SZ')
        start -= timedelta(hours=5, minutes=start_n_mins_before_close)
        stop = datetime.strptime(market_hours['closes_at'], '%Y-%m-%dT%H:%M:%SZ')
        stop -= timedelta(hours=5)
        in_range = bool(start < datetime.now() < stop)
        return bool(market_hours['is_open'] and in_range)
    except:
        return False
