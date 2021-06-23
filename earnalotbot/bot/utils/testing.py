from environ import Env
env = Env()
from earnalotbot.bot.utils.crawl_earnings_whispers import *
from earnalotbot.bot.utils.earnalotbot_main import *
from earnalotbot.bot.utils.turbulence_index import *


def test_one():
    CrawlEarningsWhispers()
    create_turbulence_index()
    earnalotbot_main(buy_time=True, hold_time=False, sell_time=False)
    earnalotbot_main(buy_time=False, hold_time=True, sell_time=False)
    earnalotbot_main(buy_time=False, hold_time=False, sell_time=True)
    earnalotbot_emergency()

def test_two():
    CrawlEarningsWhispers()
    earnalotbot_main(buy_time=True, hold_time=False, sell_time=False)
    earnalotbot_main(buy_time=False, hold_time=True, sell_time=False)
    earnalotbot_main(buy_time=False, hold_time=False, sell_time=True)
    earnalotbot_emergency()

def test_three():
    earnalotbot_main(buy_time=True, hold_time=False, sell_time=False)
    earnalotbot_main(buy_time=False, hold_time=True, sell_time=False)
    earnalotbot_main(buy_time=False, hold_time=False, sell_time=True)
    earnalotbot_emergency()


def test_four():
    earnalotbot_main(buy_time=True, hold_time=False, sell_time=False)
    earnalotbot_main(buy_time=False, hold_time=True, sell_time=False)
    earnalotbot_main(buy_time=False, hold_time=False, sell_time=True)
