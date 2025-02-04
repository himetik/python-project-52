coverage:
	pip install --upgrade pip
	pip install coverage
	source .venv/bin/activate
	coverage run --source='.' manage.py test
	coverage xml
