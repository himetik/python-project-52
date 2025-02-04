coverage:
	pip install --upgrade pip
	pip install coverage
	coverage run --source='.' manage.py test
	coverage xml
