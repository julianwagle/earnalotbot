import time

from environ import Env
from tradingview_ta import TA_Handler, Interval

from {{cookiecutter.project_slug}}.example_app.utils.ticker_tags import exchange_tag

env = Env()

def tradingview_ta_analysis(ticker, exchange, min_score=0.5, sell_multi=1):
    if not exchange:
        exchange = exchange_tag(ticker)
    analysis = TA_Handler(
        symbol=ticker,
        screener="america",
        exchange=f"{exchange}",
        interval=Interval.INTERVAL_4_HOURS,
        timeout=10
        ).get_analysis()
    tradingview_ta = {
        "summary": analysis.summary,
        "oscillators": analysis.oscillators,
        "moving_averages": analysis.moving_averages,
        "indicators": analysis.indicators
    }
    time.sleep(float(env('TV_SLEEP')))
    oscillators_rec = tradingview_ta["oscillators"]["RECOMMENDATION"]
    assert bool("BUY" in oscillators_rec)
    moving_averages_rec = tradingview_ta["moving_averages"]["RECOMMENDATION"]
    assert bool("BUY" in moving_averages_rec)
    buy = int(tradingview_ta["summary"]["BUY"])
    assert buy > 0, "No BUY Rating"
    sell = int(tradingview_ta["summary"]["SELL"]) * sell_multi
    sell = max(sell, sell_multi)
    hold = int(tradingview_ta["summary"]["NEUTRAL"])
    ratings_num = buy + sell + hold
    tradingview_ta["summary"]["SCORE"] = float(buy/ratings_num)
    assert(tradingview_ta["summary"]["SCORE"] >= min_score), "TA rating SELL"
    return tradingview_ta


def tradingview_ta_buy(ticker, exchange):
    try:
        if not exchange:
            exchange = exchange_tag(ticker)
        analysis = TA_Handler(
            symbol=ticker,
            screener="america",
            exchange=f"{exchange}",
            interval=Interval.INTERVAL_5_MINUTES,
            timeout=10
            ).get_analysis()
        time.sleep(float(env('TV_SLEEP')))
        oscillators_rec = analysis.oscillators["RECOMMENDATION"]
        moving_averages_rec = analysis.moving_averages["RECOMMENDATION"]
        return bool("BUY" in oscillators_rec and "BUY" in moving_averages_rec)
    except:
        return False

def tradingview_ta_sell(ticker, exchange):
    try:
        if not exchange:
            exchange = exchange_tag(ticker)
        analysis = TA_Handler(
            symbol=ticker,
            screener="america",
            exchange=f"{exchange}",
            interval=Interval.INTERVAL_5_MINUTES,
            timeout=10
            ).get_analysis()
        time.sleep(float(env('TV_SLEEP')))
        oscillators_rec = analysis.oscillators["RECOMMENDATION"]
        moving_averages_rec = analysis.moving_averages["RECOMMENDATION"]
        return bool("BUY" not in oscillators_rec or "BUY" not in moving_averages_rec)
    except:
        return True
