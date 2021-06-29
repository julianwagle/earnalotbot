release: python manage.py migrate
web: gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker
worker: celery worker --app=config.celery_app --loglevel=info
beat: celery beat --app=config.celery_app --loglevel=info
