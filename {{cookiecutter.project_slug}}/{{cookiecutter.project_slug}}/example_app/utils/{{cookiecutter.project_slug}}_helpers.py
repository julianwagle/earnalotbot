from environ import Env
env = Env()
from pathlib import Path
ROOT = Path(__file__).resolve(strict=True).parent.parent.parent.parent
import robin_stocks.robinhood as rh
import alpaca_trade_api
alpaca = alpaca_trade_api.REST()
from datetime import date
import time
import json
from {{cookiecutter.project_slug}}.example_app.utils.tradingview_ta_ratings import *
from {{cookiecutter.project_slug}}.example_app.utils.final_rating import *

try: upcoming_earnings = json.load(open(f"{ROOT}/data/upcoming_earnings.json"))
except: upcoming_earnings = {}

testing_bool = env.bool("TESTING", default=True)
if not testing_bool:
    cash = float(rh.account.build_user_profile()['cash'])
    time.sleep(float(env('RH_SLEEP')))
elif testing_bool:
    # alpaca is **very** slow updating wallet so i keep track on my own
    try: cash = float(json.load(open(f"{ROOT}/data/wallet.json")))
    except: cash = 1000000.00

def projected_winners(max_buys):
    potential_buys = {}
    for ticker in upcoming_earnings:
        print(ticker)
        try:
            upcoming_earnings[ticker]['tradingview_ta'] = tradingview_ta_analysis(
                ticker, upcoming_earnings[ticker]['exchange']
                )
            upcoming_earnings[ticker]['overall_score'] = final_rating(
                upcoming_earnings[ticker]
                )
            potential_buys[ticker] = upcoming_earnings[ticker]
        except: pass
    sorted_projected_winners = sorted(
        potential_buys, key=lambda x: (
            potential_buys[x]['overall_score']
            ), 
        reverse=True
        )
    return sorted_projected_winners[:max_buys]

def profitable_holdings(current_holdings_dict, min_profit):
    profitable_holdings = []
    for ticker in current_holdings_dict:
        if bool(float(current_holdings_dict[ticker]['equity_change']) >= min_profit):
            profitable_holdings.append(ticker)
    return profitable_holdings

def projected_loss_soon(ticker):
    try:return tradingview_ta_sell(ticker, upcoming_earnings[ticker]['exchange'])
    except:return tradingview_ta_sell(ticker, None)

def earnings_coming_soon(ticker):
    if ticker in upcoming_earnings:
        try:
            return bool(upcoming_earnings[ticker]['date'] == date.today().strftime("Y-%m-%d"))
        except:
            return True
    else: return False

def monetary_allocation_experiment_one(buy_list):
    print('current cash: $', cash)
    return round(float(cash/len(buy_list)))

def monetary_allocation_experiment_two(pie_slicer=0.33):
    print('current cash: $', cash)
    return round(float(cash*pie_slicer))

def purchasing_power(min_purchase_power=0.10):
    print('current cash: $', cash)
    return cash >= min_purchase_power