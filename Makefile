SHELL := /bin/bash
check: lint test

lint:
	source bin/activate && flake8 murmuration
	source bin/activate && flake8 tests
	source bin/activate && pylint --rcfile murmuration.pylintrc murmuration
	source bin/activate && pylint --rcfile tests.pylintrc tests

test:
	source bin/activate \
	  && python -B -O -m pytest \
		   --durations 10 \
		   --cov murmuration --cov-report term-missing tests/

setup:
	if which python3.7 >/dev/null && [ ! -d bin ] ; then python3.7 -m venv . ; fi
	if which python3.6 >/dev/null && [ ! -d bin ] ; then python3.6 -m venv . ; fi
	source bin/activate \
	  && python -m pip install -q -U pip \
	  && pip install -q -r requirements.txt

build:
	source bin/activate \
	  && python -B -O setup.py sdist \
	  && python -B -O setup.py bdist_wheel

clean:
	source bin/activate \
	  && python -B -O setup.py clean
	rm -rf build dist

upload:
	source bin/activate \
	  && twine upload dist/*

deploy: clean build upload

