from environ import Env
env = Env()
from earnalotbot.bot.utils.robinhood_login import *
robinhood_login()

import robin_stocks.robinhood as rh

from earnalotbot.bot.utils.market_hours import *
from earnalotbot.bot.utils.robinhood_orders import *
from earnalotbot.bot.utils.earnalotbot_helpers import *
from earnalotbot.bot.utils.robinhood_ratings import *
from earnalotbot.bot.utils.tradingview_ta_ratings import *

import sys
import time


def earnalotbot_main(
        max_buys=10, min_profit=0.01, allocation_style='two', 
        buy_time=buy_time(), hold_time=hold_time(), sell_time=sell_time()
        # adding time funcs here for testing ease. Not aesthetics haha.
    ):

    current_holdings_dict = rh.account.build_holdings()
    time.sleep(float(env('RH_SLEEP')))
    current_holdings_list = [ticker for ticker in current_holdings_dict]       
    profitable_holdings_list = profitable_holdings(current_holdings_dict, min_profit)

    if buy_time:
        projected_winners_list = projected_winners(max_buys)
        print(projected_winners_list)
        sell_list = [ticker for ticker in profitable_holdings_list if ticker not in projected_winners_list]
        for ticker in sell_list:
            sell(ticker)

        if purchasing_power():
            if allocation_style == "one":
                buy_list = [ticker for ticker in projected_winners_list if ticker not in current_holdings_list]
                for ticker in buy_list:
                    buy_size = monetary_allocation_experiment_one(buy_list)
                    buy(ticker, buy_size)

            elif allocation_style == "two":
                for ticker in projected_winners_list:
                    buy_size = monetary_allocation_experiment_two()
                    buy(ticker, buy_size)

    elif hold_time:
        for ticker in current_holdings_dict:
            if ticker in profitable_holdings_list and projected_loss_soon(ticker):
                sell(ticker)

    elif sell_time:
        for ticker in current_holdings_dict:
            if ticker in profitable_holdings_list and projected_loss_soon(ticker):
                sell(ticker)
            elif earnings_coming_soon(ticker):
                sell(ticker)

    else: print("The market it closed today. Might be a holiday. Go celebrate!")



# TODO: I have yet to determine what constitutes an emergency haha I guess I made this a little pre-empively
def earnalotbot_emergency(emergency_safe_havens={'GLD':0.2, 'SLV':0.2, 'DKNG':0.2, 'KO':0.2}, emergency_allocation_style='two'):
    current_holdings_dict = rh.account.build_holdings()
    time.sleep(float(env('RH_SLEEP')))
    for ticker in current_holdings_dict:
        sell(ticker)

    if emergency_allocation_style == 'zero':
        sys.exit()
        # creat function to turn off container

    if emergency_allocation_style == 'one':
        cash = float(rh.account.build_user_profile()['cash'])
        time.sleep(float(env('RH_SLEEP')))
        for ticker in emergency_safe_havens:
            buy_size = cash * emergency_safe_havens[ticker]
            buy(ticker, buy_size)

    elif emergency_allocation_style == 'two': # Absolutely insane
        while True:
            try:
                current_holdings_dict = rh.account.build_holdings()
                time.sleep(float(env('RH_SLEEP')))
                for ticker in current_holdings_dict:
                    if tradingview_ta_sell(ticker, exchange=False):
                        sell(ticker)
            except: pass
            
            top_movers_list = rh.markets.get_top_movers() # len = 2
            time.sleep(float(env('RH_SLEEP')))
            for mover in top_movers_list:
                ticker = mover['symbol']
                if tradingview_ta_buy(ticker, exchange=False) and robinhood_rating_buy(ticker):
                    buy_size = monetary_allocation_experiment_two()
                    buy(ticker, buy_size)

