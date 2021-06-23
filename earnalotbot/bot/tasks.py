from config import celery_app
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from datetime import datetime

from earnalotbot.bot.utils.crawl_earnings_whispers import *
from earnalotbot.bot.utils.earnalotbot_main import *
from earnalotbot.bot.utils.turbulence_index import *

def print_time():
    now = datetime.now().strftime('%Y %b %d %a @%H:%M')
    print(f'The date and time is: {now}')

# PeriodicTask.objects.all().delete()
# CrontabSchedule.objects.all().delete()

try:c0, _ = CrontabSchedule.objects.get_or_create(minute='*/1')
except Exception as e: print(e)
@celery_app.task(name='t0')
def zero():
    print_time()
try:t0 = PeriodicTask.objects.get_or_create(crontab=c0, name='t0', task='t0')
except Exception as e: print(e)

try:c1, _ = CrontabSchedule.objects.get_or_create(minute=5, hour=0)
except Exception as e: print(e)
@celery_app.task(name='t1')
def one():
    CrawlEarningsWhispers()
    create_turbulence_index()
try:t1 = PeriodicTask.objects.get_or_create(crontab=c1, name='t1', task='t1')
except Exception as e: print(e)

try:c2, _ = CrontabSchedule.objects.get_or_create(minute='*/2', hour='7-15', day_of_week='mon-fri')
except Exception as e: print(e)
@celery_app.task(name='t2')
def two():
    earnalotbot_main()
try:t2 = PeriodicTask.objects.get_or_create(crontab=c2, name='t2', task='t2')
except Exception as e: print(e)

