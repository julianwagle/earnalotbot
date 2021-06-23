from environ import Env
env = Env()

from earnalotbot.bot.utils.ticker_tags import *

from tradingview_ta import TA_Handler, Interval

import time

def tradingview_ta_analysis(ticker, exchange, min_score=0.5, sell_multi=1, hold_div=2):
    if not exchange: exchange = exchange_tag(ticker)
    analysis = TA_Handler(symbol=ticker,screener="america",exchange=f"{exchange}",interval=Interval.INTERVAL_4_HOURS,timeout=10).get_analysis()
    time.sleep(float(env('TV_SLEEP')))
    tradingview_ta = {
        "summary": analysis.summary,
        "oscillators": analysis.oscillators,
        "moving_averages": analysis.moving_averages,
        "indicators": analysis.indicators
    }
    buy = int(tradingview_ta["summary"]["BUY"])
    assert buy > 0, "No BUY Rating"
    sell = int(tradingview_ta["summary"]["SELL"]) * sell_multi
    if sell < sell_multi:
        sell = sell_multi
    hold = int(tradingview_ta["summary"]["NEUTRAL"]) / hold_div
    ratings_num = buy + sell + hold
    tradingview_ta["summary"]["SCORE"] = float(buy/ratings_num)
    assert(tradingview_ta["summary"]["SCORE"] >= min_score), "TA rating SELL"

    return tradingview_ta


def tradingview_ta_buy(ticker, exchange):
    try:
        if not exchange: exchange = exchange_tag(ticker)
        analysis = TA_Handler(symbol=ticker,screener="america",exchange=f"{exchange}",interval=Interval.INTERVAL_5_MINUTES,timeout=10).get_analysis()
        time.sleep(float(env('TV_SLEEP')))
        rec = analysis.summary["RECOMMENDATION"]
        return bool("BUY" in rec)
    except: return False

def tradingview_ta_sell(ticker, exchange):
    try:
        if not exchange: exchange = exchange_tag(ticker)
        analysis = TA_Handler(symbol=ticker,screener="america",exchange=f"{exchange}",interval=Interval.INTERVAL_5_MINUTES,timeout=10).get_analysis()
        time.sleep(float(env('TV_SLEEP')))
        rec = analysis.summary["RECOMMENDATION"]
        return bool("SELL" in rec or "NEUTRAL" in rec)
    except: return True