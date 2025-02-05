### Hexlet tests and linter status:
[![Actions Status](https://github.com/himetik/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/himetik/python-project-52/actions)

[![Maintainability](https://api.codeclimate.com/v1/badges/91aa91b43780aea51d35/maintainability)](https://codeclimate.com/github/himetik/python-project-52/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/91aa91b43780aea51d35/test_coverage)](https://codeclimate.com/github/himetik/python-project-52/test_coverage)

[![Lint and Test](https://github.com/himetik/python-project-52/actions/workflows/lint-and-test.yml/badge.svg)](https://github.com/himetik/python-project-52/actions)

https://python-project-52-ywus.onrender.com/

# Local installation for Debian/Ubuntu

```sh
# git have to be installed and ssh connection is setting up
git clone git@github.com:himetik/python-project-52.git && cd python-project-52
```

```sh
# curl have to be installed
curl -LsSf https://astral.sh/uv/install.sh | sh && export PATH="$HOME/.local/bin:$PATH"
```

```sh
# dependencies installation
uv venv && source .venv/bin/activate && uv pip install .
```

```sh
# .env should include this variables
DATABASE_URL=sqlite:///lite.db
SECRET_KEY=generate_your_own_secret_key
```

```sh
# python have to be installed
python manage.py migrate
```

```sh
# launch local host
python manage.py runserver
```
