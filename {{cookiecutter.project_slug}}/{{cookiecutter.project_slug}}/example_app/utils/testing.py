from environ import Env
env = Env()
from {{cookiecutter.project_slug}}.example_app.utils.crawl_earnings_whispers import *
from {{cookiecutter.project_slug}}.example_app.utils.{{cookiecutter.project_slug}}_main import *
from {{cookiecutter.project_slug}}.example_app.utils.turbulence_index import *

def test_one():
    CrawlEarningsWhispers()
    create_turbulence_index()
    {{cookiecutter.project_slug}}_main(
        buy_time=True, hold_time=False, sell_time=False
        )
    {{cookiecutter.project_slug}}_main(
        buy_time=False, hold_time=True, sell_time=False
        )
    {{cookiecutter.project_slug}}_main(
        buy_time=False, hold_time=False, sell_time=True
        )
    # {{cookiecutter.project_slug}}_emergency()

def test_two():
    CrawlEarningsWhispers()
    {{cookiecutter.project_slug}}_main(
        buy_time=True, hold_time=False, sell_time=False
        )
    {{cookiecutter.project_slug}}_main(
        buy_time=False, hold_time=True, sell_time=False
        )
    {{cookiecutter.project_slug}}_main(
        buy_time=False, hold_time=False, sell_time=True
        )
    # {{cookiecutter.project_slug}}_emergency()

def test_three():
    {{cookiecutter.project_slug}}_main(
        buy_time=True, hold_time=False, sell_time=False
        )
    {{cookiecutter.project_slug}}_main(
        buy_time=False, hold_time=True, sell_time=False
        )
    {{cookiecutter.project_slug}}_main(
        buy_time=False, hold_time=False, sell_time=True
        )
    # {{cookiecutter.project_slug}}_emergency()


def test_four():
    {{cookiecutter.project_slug}}_main(
        buy_time=True, hold_time=False, sell_time=False
        )
    {{cookiecutter.project_slug}}_main(
        buy_time=False, hold_time=True, sell_time=False
        )
    {{cookiecutter.project_slug}}_main(
        buy_time=False, hold_time=False, sell_time=True
        )
