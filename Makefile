VENV := .venv
VENV_PY := $(VENV)/bin/python
PY_BOOT := $(shell command -v python3.12 2>/dev/null || command -v python3.11 2>/dev/null || command -v python3 2>/dev/null)

ifeq ($(wildcard $(VENV)/bin/python),)
  PYTHON ?= python3
  PIP ?= $(PYTHON) -m pip
else
  PYTHON ?= $(VENV_PY)
  PIP ?= $(VENV_PY) -m pip
endif

.PHONY: help sync build clean install-tools upload publish env-init venv dev-install dev-install-packages env-check

help: ## Show available targets
	@grep -E '^[a-zA-Z0-9_-]+:.*## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

sync: ## Sync VERSION into each packages/*/pyproject.toml
	$(PYTHON) scripts/sync-versions.py

build: ## Build wheels/sdists for all packages
	scripts/build-all.sh

clean: ## Remove packages/*/dist build artifacts
	rm -rf packages/*/dist

install-tools: ## Install build and twine
	$(PIP) install build twine

upload: ## Upload dist/* to GitHub Packages (requires TWINE_* env)
	scripts/upload-all.sh

publish: ## Build and publish all packages
	scripts/publish-all.sh

env-init: ## Create .env from .env.example if missing
	@test -f .env || cp .env.example .env
	@echo "Environment file ready: .env (edit secrets before use)"

venv: env-init ## Create .venv and install packages for IDE use
	@if [ ! -x "$(VENV_PY)" ]; then \
		echo "Creating $(VENV) with $(PY_BOOT)"; \
		"$(PY_BOOT)" -m venv "$(VENV)"; \
	fi
	$(VENV_PY) -m pip install --upgrade pip
	$(VENV_PY) -m pip install -r requirements-dev.txt
	@echo "IDE interpreter: $(CURDIR)/$(VENV_PY)"

dev-install: venv ## Alias for venv (IDE + .env setup)

dev-install-packages: venv ## Alias for venv

env-check: ## Verify .env loads and settings parse
	$(PYTHON) scripts/from_env.py
