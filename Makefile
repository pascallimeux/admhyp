CWD=$(shell pwd)
ENV=$(CWD)/.venv

setup:
	@ sudo apt-get update && apt-get install -y openssh-server
	@ apt-get install -y build-essential python-dev gcc
	@ apt-get install -y libpq-dev libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev libffi-dev

cleandb:
	@ if [ -f "./db/admhyp.db" ]; then rm -rf ./db/admhyp.db; fi
	@ echo "Sqlite3 database removed!"

cleanpyc:
	@ find . -name '*.pyc' -exec rm -f {} +
	@ find . -name '*.pyo' -exec rm -f {} +
	@ find . -name '*~' -exec rm -f {} +

cleanenv:
	@ if [ -d ".venv" ]; then rm -rf .venv; fi
	@ echo "Python virtual env removed!"

removefolders:
	@ if [ -d "log" ]; then rm -rf log; fi
	@ if [ -d "db" ]; then rm -rf db; fi
	@ if [ -d "run" ];then rm -rf run; fi
	@ if [ -d "keys" ]; then rm -rf keys; fi
	@ echo "Folders removed!"

clean: cleanenv cleandb cleanpyc removefolders

createfolders: removefolders
	@ mkdir log
	@ mkdir db
	@ mkdir run
	@ echo "Folders created!"

initdb: cleandb
	@ PYTHONPATH=$(CWD)/src $(ENV)/bin/python -m initDB
	@ echo "Sqlite3 database initialized!"

initenv: cleanenv
	@ python3.5 -m venv $(ENV)
	@ echo "Python virtualenv installing..."
	@ $(ENV)/bin/pip install -r $(CWD)/requirements.txt 1> /dev/null 2>&1
	@ $(ENV)/bin/pip list

init: createfolders initenv initdb

logs:
	@ docker logs admhyp1 -f --tail=100

start:
	@ PYTHONPATH=$(CWD)/src $(ENV)/bin/python -m run -p 5000

docker: cleanpyc createfolders initdb
	@ if [ ! -d "keys" ]; then mkdir keys; fi
	@ ssh-keygen -t rsa -P "" -f ./keys/id_rsa -q
	@ echo "Docker image building..."
	@ docker build -t admhyp . 1> /dev/null 2>&1
	@ if [ -d keys ]; then rm -rf keys; fi
	@ echo "Docker image created!"
	@ docker images |grep admhyp

start-container:
	@ docker ps -q --filter "name=admhyp1" |grep -q . && docker stop admhyp1 && docker rm -fv admhyp1 || true
	@ docker run -d -p 8080:8080 --name admhyp1 admhyp


help:
	@echo ""
	@echo ""
	@echo ""
	@echo "     init ............. Create Python env with dependencies, folders (log, db) and init DB."
	@echo "     initenv .......... Create Python env with dependencies."
	@echo "     initdb ........... Init sqlite DB with admin account."
	@echo "     docker ........... Build docker image of the python application."
	@echo "     clean ............ Remove python virtualenv, sqlite3 DB and pyc files."
	@echo "     cleandb .......... Remove sqlite3 DB."
	@echo "     cleanpyc ......... Remove .pyc files."
	@echo "     start ............ Start application."
	@echo "     start-container .. Start the docker container of the python application."
	@echo "     logs ............. Display logs of the docker container."
	@echo ""
	@echo ""
	@echo ""
