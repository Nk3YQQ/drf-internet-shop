runserver:
	python3 manage.py runserver 0.0.0.0:8000

worker:
	celery -A config worker --loglevel=info
