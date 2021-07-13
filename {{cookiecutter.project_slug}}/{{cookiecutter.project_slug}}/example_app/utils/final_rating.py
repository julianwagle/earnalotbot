from environ import Env

env = Env()

def final_rating(
    ticker,
    fundamental_rating_multi=1,
    ta_rating_multi=1,
    ):
    fundamental = ticker['robinhood_rating']['ratings_overall'] * fundamental_rating_multi
    ta = ticker['tradingview_ta']['summary']['SCORE'] * ta_rating_multi
    rating = float(fundamental * ta )
    print('rating',rating)
    return rating
