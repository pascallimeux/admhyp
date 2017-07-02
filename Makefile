CWD=$(shell pwd)
ENV=$(CWD)/.venv

cleandb:
	rm -rf ./db/admhyp.db

cleanpyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

cleanenv:
	rm -rf .venv

removefolders:
	rm -rf log
	rm -rf db

clean: cleanenv cleandb cleanpyc removefolders

createfolders: removefolders
	mkdir log
	mkdir db

initdb: cleandb
	PYTHONPATH=$(CWD)/src $(ENV)/bin/python -m initDB

initenv: cleanenv
	python3.5 -m venv $(ENV)
	$(ENV)/bin/pip install -r $(CWD)/requirements.txt
	$(ENV)/bin/pip list

init: createfolders initenv initdb

start:
	PYTHONPATH=$(CWD)/src $(ENV)/bin/python -m run

help:
	@echo ""
	@echo "     init ........ Create Python env with dependencies, folders (log, db) and init DB."
	@echo "     initenv ..... Create Python env with dependencies."
	@echo "     initdb ...... Init sqlite DB with admin account."
	@echo "     clean ....... Remove python virtualenv, sqlite3 DB and pyc files."
	@echo "     cleandb ..... Remove sqlite3 DB."
	@echo "     cleanpyc .... Remove .pyc files."
	@echo "     start ....... Start application."
	@echo ""
