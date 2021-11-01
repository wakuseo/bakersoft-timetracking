# Makefile for BakerSoft

# -------------------------------------------------------------------------------------
# Variables {{{
# -------------------------------------------------------------------------------------
SHELL		:= /usr/bin/env bash
ROOT		:= ${CURDIR}
VENV		:= $(ROOT)/.venv
ENVS		:= $(ROOT)/.envs
SCRIPTS		:= $(ROOT)/scripts
BIN			:= $(VENV)/bin
PYTHON3		:= $(BIN)/python3
PYTHON_VER	:= python3.9 # to use for virtualenv
PYTHON		:= $(PYTHON3)
BROWSER		:= /usr/bin/google-chrome-stable
COMPOSE		:= /usr/local/bin/docker-compose
APP_DIR		:= $(ROOT)/techtest
MANAGE		:= $(PYTHON) manage.py
SCRIPT		:= $(MANAGE) runscript

# Load local environment variables
include $(ENVS)/.local/.django
include $(ENVS)/.local/.postgres

# Export all variable to sub-make
export
# -------------------------------------------------------------------------------------
# }}}
# -------------------------------------------------------------------------------------

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# -------------------------------------------------------------------------------------
# LOCAL DEV {{{
# -------------------------------------------------------------------------------------

# Setup {{{
# -------------------------------------------------------------------------------------
.PHONY: start setup restart-setup

start: setup runserver # Setup the project and run the dev server

setup: install setup-db # Setup the project

.PHONY: install
install:
	$(PYTHON_VER) -m venv $(VENV) && \
		source $(BIN)/activate && \
		$(PYTHON) -m pip install -r $(CURDIR)/requirements-local.txt

.PHONY: setup-db
setup-db: ## Load db and createsuperuser
	$(MANAGE) migrate
	$(MANAGE) createsuperuser --no-input
	$(PYTHON) $(ROOT)/populate_db.py

.PHONY: clean-db
restart-db: clean-db setup-db  ## Delete then setup db

.PHONY: clean-db
clean-db:
	@rm $(ROOT)/*.sqlite3
# -------------------------------------------------------------------------------------
# }}}

# Run locals {{{
# -------------------------------------------------------------------------------------
.PHONY: runserver

runserver: django-server-sync ## Run Django server

.PHONY: browser
browser: ## Open browser
	$(BROWSER) --new-window localhost:8000

.PHONY: django-server-async
django-server-async: ## Run the Django async server
	uvicorn config.asgi:application --host 0.0.0.0 --reload --reload-dir $(APP_DIR)

.PHONY: django-server-sync
django-server-sync: ## Run the Django server
	$(MANAGE) runserver $(DJANGO_PORT)
# -------------------------------------------------------------------------------------
# }}}

# Docker {{{
# -------------------------------------------------------------------------------------
.PHONY: compose-up compose-down

compose-up:		## docker-compose up -d
	$(COMPOSE) up -d

compose-down:	## docker-compose down
	$(COMPOSE) down
# -------------------------------------------------------------------------------------
# }}}
# -------------------------------------------------------------------------------------
# }}}
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Shell {{{
# -------------------------------------------------------------------------------------
.PHONY: shell shell-plus django-shell

shell: shell-plus ## Default shell: shell-plus

shell-plus: ## Django extension shell
	$(MANAGE) shell_plus

django-shell: ## Run ipython in django shell
	$(MANAGE) shell -i ipython
# -------------------------------------------------------------------------------------
# }}}
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Test {{{
# -------------------------------------------------------------------------------------
.PHONY: test

test: coverage ## Run tests and make coverage report

.PHONY: coverage
coverage: ## Clear and run tests with coverage report
	coverage erase
	coverage run -m pytest
	coverage report -m
	coverage html

.PHONY: show-coverage
show-coverage: ## Show test coverage in the browser
	$(BROWSER) ./htmlcov/index.html
# -------------------------------------------------------------------------------------
# }}}
# -------------------------------------------------------------------------------------
