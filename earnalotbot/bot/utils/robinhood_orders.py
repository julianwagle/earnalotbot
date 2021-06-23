import robin_stocks.robinhood as rh
import uuid
import time
from earnalotbot.bot.models import Transaction
from environ import Env
env = Env()

holdings = rh.account.build_holdings()
time.sleep(float(env('RH_SLEEP')))
testing_bool = env.bool("TESTING", default=True)

def buy(ticker, transaction_total): # ta_ratings
    if not testing_bool: 
        rh.orders.order_buy_fractional_by_price(
            symbol=ticker, amountInDollars=transaction_total
        )
        time.sleep(float(env('RH_SLEEP')))
    quote = rh.stocks.get_quotes(ticker)[0]
    time.sleep(float(env('RH_SLEEP')))
    Transaction.objects.create(
        transaction_code = uuid.uuid1(),
        action = "B",
        symbol = ticker,
        share_price = float(quote['last_trade_price']),
        share_quant = float(transaction_total/float(quote['last_trade_price'])),
        share_equity = transaction_total,
        roi_total = 0,
        roi_net =  0,
        # ta_ratings = ta_ratings,
        testing = testing_bool
    )
    transactions = Transaction()
    transactions.save()
    print(f"Buying {ticker} @ ${float(quote['last_trade_price'])} with ${transaction_total}.")

def hold(ticker): # ta_ratings
    Transaction.objects.create(
        transaction_code = uuid.uuid1(),
        action = 'H',
        symbol = ticker,
        share_price = holdings[ticker]['price'],
        share_quant = holdings[ticker]['quantity'],
        share_equity = holdings[ticker]['equity'],
        roi_total = holdings[ticker]['percent_change'],
        roi_net =  holdings[ticker]['equity_change'],
        # ta_ratings = ta_ratings,
        testing = testing_bool
    )
    transactions = Transaction()
    transactions.save()
    print(f"Holding {ticker} with a {holdings[ticker]['percent_change']}% change in value and a rating of <add ratings to db>.")

def sell(ticker): # ta_ratings
    if not testing_bool: 
        rh.orders.order_sell_fractional_by_quantity(
            symbol=ticker, quantity=float(holdings[ticker]['quantity'])
        )
        time.sleep(float(env('RH_SLEEP')))
    Transaction.objects.create(
        transaction_code = uuid.uuid1(),
        action = 'S',
        symbol = ticker,
        share_price = holdings[ticker]['price'],
        share_quant = holdings[ticker]['quantity'],
        share_equity = holdings[ticker]['equity'],
        roi_total = holdings[ticker]['percent_change'],
        roi_net =  holdings[ticker]['equity_change'],
        # ta_ratings = ta_ratings,
        testing = testing_bool
    )
    transactions = Transaction()
    transactions.save()
    print(f"Selling ${holdings[ticker]['quantity']} worth of {ticker} for a final return of {holdings[ticker]['percent_change']}%.")


