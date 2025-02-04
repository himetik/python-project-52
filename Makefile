coverage:
    pip install coverage
    coverage run --source='.' manage.py test
    coverage xml
