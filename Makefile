.PHONY: install develop wsgi migrate


PIP?=pip2
PYTHON=python2

install:
	$(PIP) install -r requirements.txt

migrate:
	$(PYTHON) application.py db upgrade head

run:
	$(PYTHON) wsgi.py

develop:
	$(PYTHON) application.py runserver
