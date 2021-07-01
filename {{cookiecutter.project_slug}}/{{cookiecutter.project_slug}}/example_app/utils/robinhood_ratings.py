import time

import robin_stocks.robinhood as rh

from environ import Env

env = Env()

def robinhood_rating_summary(ticker, min_score=.5, sell_multi=1):
    rating = rh.stocks.get_ratings(ticker)
    time.sleep(float(env('RH_SLEEP')))
    buy = int(rating["summary"]["num_buy_ratings"])
    assert buy > 0, "No BUY Rating"
    sell = int(rating["summary"]["num_sell_ratings"]) + int(rating["summary"]["num_hold_ratings"])
    sell *= sell_multi
    sell = max(sell, sell_multi)
    ratings_num = buy + sell
    rating["summary"]["ratings_overall"] = float(buy/ratings_num)
    assert(rating["summary"]["ratings_overall"] >= min_score), "Fundamental rating SELL"
    return rating["summary"]

def robinhood_rating_buy(ticker, min_score=.5):
    try:
        rating = rh.stocks.get_ratings(ticker)
        time.sleep(float(env('RH_SLEEP')))
        buy = int(rating["summary"]["num_buy_ratings"])
        sell = int(rating["summary"]["num_sell_ratings"]) + int(rating["summary"]["num_hold_ratings"])
        ratings_num = buy + sell
        return bool(float(buy/ratings_num) >= min_score)
    except:
        return False
