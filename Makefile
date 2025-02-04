coverage:
	pip install --upgrade pip
	pip install coverage
	python -m venv .venv
	. .venv/bin/activate
	coverage run --source='.' manage.py test
	coverage xml
