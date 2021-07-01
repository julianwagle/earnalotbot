from pathlib import Path

from environ import Env

env = Env()
APP = Path(__file__).resolve(strict=True).parent.parent

def size_tag(ticker):
    codes = ['mega','large','medium','small','micro',]
    for code in codes:
        data = eval(open(f"{APP}/data/tags/{code}.txt", "r").read())
        if ticker in data:
            return code

def industry_tag(ticker):
    tags = []
    codes = [
        'basic', 'capital', 'durables', 'energy', 'finance', 'health', 
        'misc', 'nondurables', 'services', 'techno', 'transport', 'utils'
        ]
    for code in codes:
        data = eval(open(f"{APP}/data/tags/{code}.txt", "r").read())
        if ticker in data:
            tags.append(code)
    return tags

def exchange_tag(ticker):
    codes = ['nasdaq', 'amex', 'nyse']
    for code in codes:
        data = eval(open(f"{APP}/data/tags/{code}.txt", "r").read())
        if ticker in data:
            return code
