release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn my_portfolio.wsgi --preload --log-file -