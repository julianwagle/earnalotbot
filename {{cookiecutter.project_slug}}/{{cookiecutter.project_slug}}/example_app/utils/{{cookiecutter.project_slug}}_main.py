import time

import robin_stocks.robinhood as rh
import alpaca_trade_api

from environ import Env

from {{cookiecutter.project_slug}}.example_app.utils.robinhood_login import robinhood_login
from {{cookiecutter.project_slug}}.example_app.utils.market_hours import get_buy_time, get_hold_time, get_sell_time
from {{cookiecutter.project_slug}}.example_app.utils.orders import buy, sell
from {{cookiecutter.project_slug}}.example_app.utils.{{cookiecutter.project_slug}}_helpers import (
    get_current_holdings,
    profitable_holdings,
    projected_winners,
    projected_loss_soon,
    earnings_coming_soon,
    purchasing_power,
    monetary_allocation_experiment_one,
    monetary_allocation_experiment_two,
    set_testing_cash,
    top_movers,
)
from {{cookiecutter.project_slug}}.example_app.utils.robinhood_ratings import robinhood_rating_buy
from {{cookiecutter.project_slug}}.example_app.utils.tradingview_ta_ratings import tradingview_ta_buy, tradingview_ta_sell

env = Env()
testing_bool = env.bool("TESTING", default=True)
alpaca = alpaca_trade_api.REST()

robinhood_login()

if testing_bool:
    set_testing_cash()


def {{cookiecutter.project_slug}}_main(
        max_buys=10, min_profit=0.01, allocation_style='two',
        buy_time=get_buy_time(), hold_time=get_hold_time(), sell_time=get_sell_time()
        # adding time funcs here for testing ease. Not aesthetics haha.
    ):
    current_holdings_dict = get_current_holdings()
    current_holdings = bool(len(current_holdings_dict))
    if current_holdings:
        profitable_holdings_list = profitable_holdings(current_holdings_dict, min_profit)

    if buy_time:
        projected_winners_list = projected_winners(max_buys)
        print(f'upcoming earnings projected winners: {projected_winners_list}')
        if len(projected_winners_list) < 5:
            print('getting extras from top movers ...')
            grab_len = max_buys - len(projected_winners_list)
            projected_winners_list += top_movers(grab_len)

        print('complete projected winners list:',projected_winners_list)

        if current_holdings:
            sell_list = [ticker for ticker in profitable_holdings_list if ticker not in projected_winners_list]
            for ticker in sell_list:
                sell(ticker, current_holdings_dict)
            print('sell list:',sell_list)

        if purchasing_power():
            print("pruchasing_power() = True")
            for ticker in projected_winners_list:
                if allocation_style == "one":
                    buy_size = monetary_allocation_experiment_one(projected_winners_list)
                elif allocation_style == "two":
                    buy_size = monetary_allocation_experiment_two()
                buy(ticker, buy_size)

    elif hold_time and current_holdings:
        for ticker in current_holdings_dict:
            if ticker in profitable_holdings_list and projected_loss_soon(ticker):
                sell(ticker, current_holdings_dict)

    elif sell_time and current_holdings:
        for ticker in current_holdings_dict:
            if ticker in profitable_holdings_list and projected_loss_soon(ticker):
                sell(ticker, current_holdings_dict)
            elif earnings_coming_soon(ticker):
                sell(ticker, current_holdings_dict)

    else: print("The market is closed. Might be a holiday. Go celebrate!")


