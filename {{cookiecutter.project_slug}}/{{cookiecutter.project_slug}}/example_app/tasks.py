from datetime import datetime

from django_celery_beat.models import CrontabSchedule, PeriodicTask

from config import celery_app
from {{cookiecutter.project_slug}}.example_app.utils.crawl_earnings_whispers import CrawlEarningsWhispers
from {{cookiecutter.project_slug}}.example_app.utils.{{cookiecutter.project_slug}}_main import {{cookiecutter.project_slug}}_main

def print_time():
    now = datetime.now().strftime('%Y %b %d %a @%H:%M')
    print(f'The date and time is: {now}')

# docker-compose -f local.yml up
# docker-compose -f local.yml run django python manage.py shell
# from django_celery_beat.models import CrontabSchedule, PeriodicTask; PeriodicTask.objects.all().delete();CrontabSchedule.objects.all().delete()

c0, _ = CrontabSchedule.objects.get_or_create(minute='*/1')
c1, _ = CrontabSchedule.objects.get_or_create(minute=5, hour=0)
c2, _ = CrontabSchedule.objects.get_or_create(minute='*/2', hour='7-15', day_of_week='mon-fri')

@celery_app.task(name='t0')
def zero():
    print_time()

@celery_app.task(name='t1')
def one():
    print_time()
    CrawlEarningsWhispers()

@celery_app.task(name='t2')
def two():
    print_time()
    {{cookiecutter.project_slug}}_main()

t0 = PeriodicTask.objects.get_or_create(crontab=c0, name='t0', task='t0')
t1 = PeriodicTask.objects.get_or_create(crontab=c1, name='t1', task='t1')
t2 = PeriodicTask.objects.get_or_create(crontab=c2, name='t2', task='t2')
