from environ import Env

env = Env()

def final_rating(
    ticker,
    fundamental_rating_multi=1,
    ta_rating_multi=1,
    downside_deviation_power=2
    ):
    fundamental = ticker['robinhood_rating']['ratings_overall'] * fundamental_rating_multi
    ta = ticker['tradingview_ta']['summary']['SCORE'] * ta_rating_multi
    downside_deviation = ticker['downside_deviation'] ** downside_deviation_power
    rating = float(fundamental * ta ) / downside_deviation
    return rating
