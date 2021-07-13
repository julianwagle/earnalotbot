import random
import time
import json
import re

from datetime import datetime, date, timedelta
from pathlib import Path

from environ import Env
from bs4 import BeautifulSoup as bs
from selenium import webdriver

from {{cookiecutter.project_slug}}.example_app.utils.ticker_tags import exchange_tag
from {{cookiecutter.project_slug}}.example_app.utils.robinhood_ratings import robinhood_rating_summary

env = Env()
ROOT = Path(__file__).resolve(strict=True).parent.parent.parent.parent
APP = Path(__file__).resolve(strict=True).parent.parent

class CrawlEarningsWhispers:
    def __init__(self, end_date=10, start_date=-1):
        selenium_options = webdriver.ChromeOptions()
        selenium_options.add_argument("start-maximized")
        selenium_options.add_argument("disable-infobars")
        selenium_options.add_argument("--disable-extensions")
        selenium_options.add_argument("--no-sandbox")
        selenium_options.add_argument("--headless")
        # https://stackoverflow.com/questions/53902507/unknown-error-session-deleted-because-of-page-crash-from-unknown-error-cannot
        selenium_options.add_argument('--disable-dev-shm-usage')
        ubuntu_driver_loc = f'{APP}/utils/chromedriver_ubuntu'
        self.selenium_driver = webdriver.Chrome(
            executable_path=ubuntu_driver_loc, options=selenium_options
            )
        self.trading_days = []
        self.link_list_counter=start_date
        self.link_list_max=end_date
        self.main_data = {}
        self.move_around()

    def move_around(self):
        try:
            self.link_list_counter += 1
            assert(self.link_list_max >= self.link_list_counter), "Mission accomplished. Head out!"
            self.selenium_driver.get(
                f"https://www.earningswhispers.com/calendar?sb=p&d={self.link_list_counter}&t=all&v=t"
                )
            time.sleep(round(random.uniform(2, 7), 4))
            self.get_page_data()
            self.move_around()
        except:
            self.selenium_driver.quit()
            assert isinstance(self.main_data, dict), "Failed the final type test... so close!"
            print(self.main_data)     
            json.dump(self.main_data, open(f"{ROOT}/data/upcoming_earnings.json", "w"))

    def get_page_data(self):
        try:
            current_page_source = self.selenium_driver.page_source
            page_html = bs(current_page_source, 'html.parser')
            page_data = page_html.find_all("li", class_=["showconf", "shownotconf"])
            if len(page_data):
                month = str(page_html.find(class_="month").string)
                day = str(page_html.find(class_="day").string)
                earn_date = datetime.strptime(str(month + day), "%B%d") # timedelta
                earn_date = earn_date.strftime("%m-%d") # "02-08-1900"
                earn_date = datetime.strptime(earn_date, "%m-%d") # timedelta
                today = date.today() # timedelta 2021-02-08 (%Y-%m-%d)
                moving_date = today # starts at today ... moves to earn mon & day to get yyyy
                days_to_earn = 0 # default/starting value
                failure = True # default/starting value
                while failure and self.link_list_max >= days_to_earn:
                    try:
                        assert(moving_date.day == earn_date.day), "Wrong day"
                        assert(moving_date.month == earn_date.month), "Wrong month"
                        failure = False # Breaks while loop
                    except:
                        moving_date += timedelta(days=1) # Try the following day
                        days_to_earn += 1
                if moving_date.strftime("%Y-%m-%d") not in self.trading_days:
                    self.trading_days.append(moving_date.strftime("%Y-%m-%d")) # string
                    for stock in page_data:
                        print(self.trading_days)
                        earnings_date = self.trading_days[-1]
                        try:
                            ticker = stock.find(class_="ticker").string
                            projd_growth_string = stock.find(class_="revgrowthprint").string
                            projd_growth_stripped = str(projd_growth_string).replace('%','')
                            projd_growth_float = float(projd_growth_stripped)
                            assert  0 < projd_growth_float < float('inf')
                            earnings_time = stock.find(class_="time").string
                            amc = bool(re.search("AMC", earnings_time) or re.search("PM ET", earnings_time))
                            if not amc:
                                assert len(self.trading_days) > 1
                                earnings_date = self.trading_days[-2]
                            exchange = exchange_tag(ticker)
                            test = {
                                "date": earnings_date,
                                "projd_growth": projd_growth_float,
                                "exchange": exchange,
                                "robinhood_rating": robinhood_rating_summary(ticker),
                            }
                            assert isinstance(test, dict), "Failed type test"
                            print(test)
                            self.main_data[ticker] = test
                        except: 
                            pass
        except Exception as e: 
            print(f"Exception: {e}")