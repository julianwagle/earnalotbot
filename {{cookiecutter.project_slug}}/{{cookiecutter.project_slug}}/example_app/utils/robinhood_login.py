from environ import Env
env = Env()
import robin_stocks.robinhood as rh
from robin_stocks.robinhood.globals import *
from pyotp import TOTP as otp
import time

def robinhood_login():
    global LOGGED_IN
    if not LOGGED_IN:
        totp = otp(env('RH_DEVICE_TOKEN')).now()
        rh.authentication.login(
            username=env('RH_USERNAME'),
            password=env('RH_PASSWORD'), 
            mfa_code=totp
        )
        print('logged in to robinhood.')
        time.sleep(float(env('RH_SLEEP')))