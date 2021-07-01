import time

import robin_stocks.robinhood as rh

from pyotp import TOTP as otp
from environ import Env

env = Env()

def robinhood_login():
    totp = otp(env('RH_DEVICE_TOKEN')).now()
    rh.authentication.login(
        username=env('RH_USERNAME'),
        password=env('RH_PASSWORD'),
        mfa_code=totp
    )
    print('logged in to robinhood.')
    time.sleep(float(env('RH_SLEEP')))
