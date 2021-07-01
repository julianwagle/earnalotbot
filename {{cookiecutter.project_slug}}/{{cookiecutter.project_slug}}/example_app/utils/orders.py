import math
import uuid
import json

from pathlib import Path

import robin_stocks.robinhood as rh
import alpaca_trade_api

from environ import Env

from {{cookiecutter.project_slug}}.example_app.models import Transaction
from {{cookiecutter.project_slug}}.example_app.utils.{{cookiecutter.project_slug}}_helpers import get_cash

env = Env()
testing_bool = env.bool("TESTING", default=True)
ROOT = Path(__file__).resolve(strict=True).parent.parent.parent.parent
alpaca = alpaca_trade_api.REST()


def buy(ticker, transaction_total):
    print(f"{ticker} ${transaction_total}")
    cash = get_cash()
    if not testing_bool:
        print('submitting robinhood order')
        rh.orders.order_buy_fractional_by_price(
            symbol=ticker, amountInDollars=transaction_total
        )
        print(f"buying s{transaction_total} worth of {ticker}")
        cash -= transaction_total
        quote = rh.stocks.get_quotes(ticker)[0]
        Transaction.objects.create(
            transaction_code = uuid.uuid1(),
            action = "B",
            symbol = ticker,
            share_price = float(quote['last_trade_price']),
            share_quant = float(transaction_total/float(quote['last_trade_price'])),
            share_equity = transaction_total,
            roi_total = 0,
            roi_net =  0,
            avg_buy_price = float(quote['last_trade_price']),
            testing = testing_bool
        )
    elif testing_bool:
        print('submitting alpaca order')
        asset = alpaca.get_asset(ticker)
        if not asset.fractionable:
            quote = rh.stocks.get_quotes(ticker)[0]
            last_trade_price = float(quote['last_trade_price'])
            transaction_total = math.floor(transaction_total/last_trade_price)
            alpaca.submit_order(
                symbol=ticker, 
                qty=transaction_total,
                side='buy',type='market',time_in_force='day'
            )
            print(f"buying {transaction_total} shares of {ticker}")
            cash -= float(transaction_total * last_trade_price)
            Transaction.objects.create(
                transaction_code = uuid.uuid1(),
                action = "B",
                symbol = ticker,
                share_price = last_trade_price,
                share_quant = float(transaction_total),
                share_equity = transaction_total * last_trade_price,
                roi_total = 0,
                roi_net =  0,
                avg_buy_price = last_trade_price,
                testing = testing_bool
            )
        else:
            quote = rh.stocks.get_quotes(ticker)[0]
            last_trade_price = float(quote['last_trade_price'])
            alpaca.submit_order(
                symbol=ticker, 
                notional=transaction_total,
                side='buy',type='market',time_in_force='day'
            )
            print(f"buying s{transaction_total} worth of {ticker}")
            cash -= transaction_total
            Transaction.objects.create(
                transaction_code = uuid.uuid1(),
                action = "B",
                symbol = ticker,
                share_price = float(quote['last_trade_price']),
                share_quant = float(transaction_total/float(quote['last_trade_price'])),
                share_equity = transaction_total,
                roi_total = 0,
                roi_net =  0,
                avg_buy_price = float(quote['last_trade_price']),
                testing = testing_bool
            )
    json.dump(cash, open(f"{ROOT}/data/wallet.json", "w"))
    transactions = Transaction()
    transactions.save()

def hold(ticker, holdings):
    holding = holdings[ticker]
    Transaction.objects.create(
        transaction_code = uuid.uuid1(),
        action = 'H',
        symbol = ticker,
        avg_buy_price = holding['average_buy_price'],
        share_price = holding['price'],
        share_quant = holding['quantity'],
        share_equity = holding['equity'],
        roi_total = holding['percent_change'],
        roi_net =  holding['equity_change'],
        testing = testing_bool
    )
    print(f"Holding {ticker} with a {holding['percent_change']}% change in value.")
    transactions = Transaction()
    transactions.save()

def sell(ticker, holdings):
    cash = get_cash()
    holding = holdings[ticker] 
    if not testing_bool:
        print('submitting robinhood order')
        rh.orders.order_sell_fractional_by_quantity(
            symbol=ticker, quantity=float(holding['quantity'])
        )
    if testing_bool:
        print('submitting alpaca order')
        alpaca.submit_order(
            symbol=ticker,
            qty=holding['quantity'],
            side='sell',
            type='market',
            time_in_force='day',
        )
    Transaction.objects.create(
        transaction_code = uuid.uuid1(),
        action = 'S',
        symbol = ticker,
        avg_buy_price = holding['average_buy_price'],
        share_price = holding['price'],
        share_quant = holding['quantity'],
        share_equity = holding['equity'],
        roi_total = holding['percent_change'],
        roi_net =  holding['equity_change'],
        testing = testing_bool
    )
    print(f"Selling ${holding['equity']} worth of {ticker} for a final return of {holding['percent_change']}%.")
    cash += float(holding['equity'])
    json.dump(cash, open(f"{ROOT}/data/wallet.json", "w"))
    transactions = Transaction()
    transactions.save()
