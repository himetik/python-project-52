locale:
	python manage.py makemessages -l ru && python manage.py compilemessages
migrate:
	python manage.py makemigrations && python manage.py migrate
localhost:
	python manage.py runserver
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	python manage.py shell -c "from django.core.cache import cache; cache.clear()"
	rm -rf ./staticfiles/
	rm -rf ./media/CACHE/
	rm -rf ./tmp/
