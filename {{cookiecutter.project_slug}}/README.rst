Earnalotbot 🤖💰
================

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django

.. image:: https://img.shields.io/github/workflow/status/pydanny/cookiecutter-django/CI/master
    :target: https://github.com/pydanny/cookiecutter-django/actions?query=workflow%3ACI
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black
    :alt: Code style: black



Project Overview
----------------

The Earnalotbot is a scaffolding for advanced python based developers looking to make trading bots. 
It comes equipped with basic packages for live-trading, paper-trading, web-scrapping, reinforcement-learning, a database for long-term strategy analysis and much more. 
Included is an extra app titled 'example_app' - it is a fully functional trading bot and act as an example of how to use and integrate the packages. 
If you're not careful to customize it to your liking or delete it, it will perform live trades if the TESTING var in .envs is set to 'False'


The default bot included follwos the general trading strategy list below:

* First, the bot finds a list of companies projected by experts to have a profitable earnings report occuring in the next ${n} days.

* Second, the bot filters through buy/sell ratings provided by experts analyzing the fundamentals of each company to filter out those with poor fundamentrals. 

* Third, the bot sorts the remaining companies by their technical indicators and fundamental analysis ratings to determine where to invest at any given moment.


The strategy is a little more nuanced than this and I have designed the code to be quickly and easily changed by anyone with a low-level understanding of Python.
This way, the bot can be adjusted to fit your temperment/risk-tolerance rather fast without too much of a headache. 

* To give the bot's strategy a quick overview simply navigate to::

    ROOT/PROJ_SLUG/example_app/utils

    
DISCALIMER
----------
Decisions to buy, sell, hold or trade in securities involve risk and are best made based on the advice of qualified financial professionals. 
Any trading in securities or other investments involves a risk of substantial losses. 
The practice of "Day Trading" involves particularly high risks and can cause you to lose substantial sums of money. 
Before using any trading software, you should consult a qualified financial professional. 
Please consider carefully whether such trading is suitable for you in light of your financial condition and ability to bear financial risks. 
Under no circumstances shall I be liable for any loss or damage you or anyone else incurs as a result of any trading or investment activity that you or anyone else engages in based on any information or material you receive through me or my code. 
There are frequently sharp differences between hypothetical performance results and actual results subsequently achieved by any particular trading program. 
The ability to withstand losses or to adhere to a particular trading program in spite of the trading losses are material points, which can also adversely affect trading results. 
There are numerous other factors related to the market in general or to the implementation of any specific trading program which cannot be fully accounted for in the preparation of hypothetical performance results and all of which can adversely affect actual trading results.


Integrations
------------

* Integration with RobinStocks_ for market data and live-trading
* Integration with Alpaca_ API for paper-trading
* Store trading data in a PostgresSQL_ database for long-term strategy evaluations.
* Scrape/Crawl relevant data from the internet with Selenium_ & BS4_
* Integrate Reinforcement learnign with Tensorflow_ and other RL packages.
* View pre-calculated technical analysis with Tradingview_TA_
* Perform custom technical analysis with data from y-finance_
* Serve static files from Amazon S3, Google Cloud Storage or Whitenoise_
* Configuration for Celery_ and Flower_ 
* Integration with MailHog_ for local email testing
* Integration with Sentry_ for error logging

.. _RobinStocks: https://www.robin-stocks.com/en/latest/
.. _Aplaca: https://alpaca.markets/
.. _PostgreSQL: https://www.postgresql.org/
.. _Selenium: https://www.selenium.dev/
.. _BS4: https://beautiful-soup-4.readthedocs.io/en/latest/
.. _Tensorflow: https://www.tensorflow.org/
.. _Y-Finance: https://github.com/ranaroussi/yfinance
.. _Bootstrap: https://github.com/twbs/bootstrap
.. _django-environ: https://github.com/joke2k/django-environ
.. _12-Factor: http://12factor.net/
.. _django-allauth: https://github.com/pennersr/django-allauth
.. _django-avatar: https://github.com/grantmcconnaughey/django-avatar
.. _Procfile: https://devcenter.heroku.com/articles/procfile
.. _Mailgun: http://www.mailgun.com/
.. _Whitenoise: https://whitenoise.readthedocs.io/
.. _Celery: http://www.celeryproject.org/
.. _Flower: https://github.com/mher/flower
.. _Anymail: https://github.com/anymail/django-anymail
.. _MailHog: https://github.com/mailhog/MailHog
.. _Sentry: https://sentry.io/welcome/
.. _docker-compose: https://github.com/docker/compose
.. _PythonAnywhere: https://www.pythonanywhere.com/
.. _Traefik: https://traefik.io/
.. _LetsEncrypt: https://letsencrypt.org/
.. _pre-commit: https://github.com/pre-commit/pre-commit

Constraints
-----------

* Only maintained 3rd party libraries are used.
* Uses PostgreSQL everywhere (10.16 - 13.2)
* Environment variables for configuration (This won't work with Apache/mod_wsgi).

Usage
------

First, get Cookiecutter. Trust me, it's awesome::

    $ pip3 install "cookiecutter>=1.7.0"

Now run it against this repo::

    $ cookiecutter https://github.com/julianwagle/earnalotbot

You'll be prompted for some values. Provide them, then a Django project will be created for you.

**Warning**: After this point, change 'Julian Wagle', 'julianwagle', etc to your own information.

Answer the prompts with your own desired options_. For example::

    me@jool-yuhns-laptop:~$ cookiecutter https://github.com/julianwagle/earnalotbot
    project_name [Earn A Lot Bot]: 
    project_slug [earn_a_lot_bot]: earnalotbot
    description [A bot that earns a lot!]: 
    author_name [Julian Wagle]: 
    domain_name [example.com]: earnalotbot.com
    email [julian-wagle@example.com]: julian.wagle@gmail.com
    version [0.1.0]: 
    Select open_source_license:
    1 - MIT
    2 - BSD
    3 - GPLv3
    4 - Apache Software License 2.0
    5 - Not open source
    Choose from 1, 2, 3, 4, 5 [1]: 
    timezone [UTC]: "America/Chicago"
    windows [n]: 
    use_pycharm [n]: 
    Select postgresql_version:
    1 - 13.2
    2 - 12.6
    3 - 11.11
    4 - 10.16
    Choose from 1, 2, 3, 4 [1]: 2
    Select cloud_provider:
    1 - AWS
    2 - GCP
    3 - None
    Choose from 1, 2, 3 [1]: 2
    Select mail_service:
    1 - Mailgun
    2 - Amazon SES
    3 - Mailjet
    4 - Mandrill
    5 - Postmark
    6 - Sendgrid
    7 - SendinBlue
    8 - SparkPost
    9 - Other SMTP
    Choose from 1, 2, 3, 4, 5, 6, 7, 8, 9 [1]: 
    custom_bootstrap_compilation [n]: y
    use_compressor [n]: y
    use_mailhog [n]: y
    use_sentry [n]: y
    use_whitenoise [n]: y
    use_heroku [n]: 
    Select ci_tool:
    1 - None
    2 - Travis
    3 - Gitlab
    4 - Github
    Choose from 1, 2, 3, 4 [1]: 4
    debug [n]: 
    [SUCCESS]: Project initialized, keep up the good work!


Enter the project and take a look around::

    $ cd earnalotbot/
    $ ls

Create a git repo and push it there::

    $ git init
    $ git add .
    $ git commit -m "first awesome commit"
    $ git remote add origin git@github.com:julianwagle/earnalotbot.git
    $ git push -u origin master

Now take a look at your repo. Don't forget to carefully look at the generated README. Awesome, right?


Pre-requisite accounts
----------------------
Before you begin, you will need accounts for the following:

Robinhood
^^^^^^^^^

Robinhood is a free trading platform. You can sign up for a free account at  https://robinhood.com/

It is requirued for running locally and in production.


Alpaca
^^^^^^

Aplaca has a great and free api for paper trading. You can sign up for a free account at  https://alpaca.markets/docs/get-started-with-alpaca/

It is requirued for running locally.



Initial Config
--------------

Integrating the bot with Robinhood's API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Much of the following section is either para-phrasing or directly quoting from the documentation for the Robin Stocks Repo's documentation. You can find more at::

    https://www.robin-stocks.com/en/latest/quickstart.html


* For this step, you will have to sign into your Robinhood account and turn on 2FA. When Robinhood asks you which 2FA app you want to use - select “other”. 

* Robinhood will present you with an alphanumeric code. This code is what you will use for “My2factorAppHere” in the code below. 

* After installing Pyotp on your machine, open up a Python terminal and run the following command::

    >>> print(pyotp.TOTP("My2factorAppHere").now())

* Type the resulting MFA code into the prompt on your Robinhood app.

* Robinhood will then give you a backup code. Make sure you **do not lose this backup code or you may be locked out of your account!** 

* You can also take the exact same “My2factorAppHere” from above and enter it into your phone’s authentication app, such as Google Authenticator. This will cause the exact same MFA code to be generated on your phone as well as your python code.  This is important to do if you plan on being away from your computer and need to access your Robinhood account from your phone.


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy earnalotbot

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html

Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd earnalotbot
    celery -A config.celery_app worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.


Email Server
^^^^^^^^^^^^

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server `MailHog`_ with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.
Please check `cookiecutter-django Docker documentation`_ for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to ``http://127.0.0.1:8025``

.. _mailhog: https://github.com/mailhog/MailHog


Deployment
----------

The following details how to deploy this application.

Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html
Custom Bootstrap Compilation
^^^^^^

The generated CSS is set up with automatic Bootstrap recompilation with variables of your choice.
Bootstrap v4 is installed using npm and customised by tweaking your variables in ``static/sass/custom_bootstrap_vars``.

You can find a list of available variables `in the bootstrap source`_, or get explanations on them in the `Bootstrap docs`_.
Bootstrap's javascript as well as its dependencies is concatenated into a single file: ``static/js/vendors.js``.

.. _in the bootstrap source: https://github.com/twbs/bootstrap/blob/v4-dev/scss/_variables.scss
.. _Bootstrap docs: https://getbootstrap.com/docs/4.1/getting-started/theming/

Code of Conduct
---------------

If you make some big bucks with this dont forget about me!
