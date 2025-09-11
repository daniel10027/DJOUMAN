.PHONY: install run migrate superuser fmt lint check

install:
\tpip install -r requirements.txt

run:
\tpython manage.py runserver

migrate:
\tpython manage.py makemigrations
\tpython manage.py migrate

superuser:
\tpython manage.py createsuperuser

fmt:
\truff check --fix || true
\tisort . && black .

lint:
\truff check .

check: lint
\tpython manage.py check
