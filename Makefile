CWD=$(shell pwd)
ENV=$(CWD)/.venv

initenv:
	python3.5 -m venv $(ENV)
	$(ENV)/bin/pip install -r $(CWD)/requirements.txt

cleandb:
	rm -rf ./db/admhyp.db

initdb:
	PYTHONPATH=$(CWD)/src $(ENV)/bin/python -m initDB

cleanpyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

start:
	PYTHONPATH=$(CWD)/src $(ENV)/bin/python -m run

help:
	@echo ""
	@echo "     initenv ..... Create Python env with dependencies."
	@echo "     initdb ...... Init sqlite DB with admin account."
	@echo "     cleandb ..... Remove sqlite DB."
	@echo "     cleanpyc .... Remove .pyc files."
	@echo "     start ....... Start application."
	@echo ""
