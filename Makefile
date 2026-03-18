# =========================================================
# Stock Prediction POC Makefile
# =========================================================

# Python runner using uv
PYTHON = uv run python

# Project directories
SRC = src
TESTS = tests
SCRIPTS = scripts
DASHBOARD = dashboard

# =========================================================
# Environment
# =========================================================

install:
	uv sync --all-extras

update:
	uv lock
	uv sync --all-extras

venv:
	uv venv

# =========================================================
# Code Quality
# =========================================================

format:
	uv run black $(SRC) $(TESTS)

lint:
	uv run ruff check $(SRC) $(TESTS)

lint-fix:
	uv run ruff check $(SRC) $(TESTS) --fix

check: format lint

# =========================================================
# Testing
# =========================================================

test:
	uv run pytest -v

test-fast:
	uv run pytest -q

coverage:
	uv run pytest --cov=$(SRC)

# =========================================================
# Data Pipelines
# =========================================================

ingest:
	$(PYTHON) $(SCRIPTS)/run_ingestion.py

features:
	$(PYTHON) $(SCRIPTS)/generate_features.py

train:
	$(PYTHON) $(SCRIPTS)/run_training.py

predict:
	$(PYTHON) $(SCRIPTS)/run_prediction.py

backtest:
	$(PYTHON) $(SCRIPTS)/run_backtest.py

pipeline:
	make ingest
	make features
	make train
	make predict

# =========================================================
# Dashboard
# =========================================================

dashboard:
	uv run streamlit run $(DASHBOARD)/streamlit_app.py

# =========================================================
# Utilities
# =========================================================

logs:
	tail -f logs/app.log

# =========================================================
# Cleaning
# =========================================================

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -rf .pytest_cache

clean-data:
	rm -rf data/processed/*
	rm -rf data/features/*

clean-all:
	make clean
	make clean-data

# =========================================================
# Development Helpers
# =========================================================

dev-setup:
	make install
	make format
	make lint

run:
	make pipeline

# =========================================================
# Help
# =========================================================

help:
	@echo "Available commands:"
	@echo ""
	@echo "Environment:"
	@echo "  make install        Install dependencies"
	@echo "  make update         Update dependencies"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format         Format code with black"
	@echo "  make lint           Lint code with ruff"
	@echo ""
	@echo "Testing:"
	@echo "  make test           Run tests"
	@echo "  make coverage       Run tests with coverage"
	@echo ""
	@echo "Pipelines:"
	@echo "  make ingest         Run data ingestion"
	@echo "  make features       Generate features"
	@echo "  make train          Train models"
	@echo "  make predict        Generate predictions"
	@echo "  make backtest       Run backtesting"
	@echo "  make pipeline       Run full pipeline"
	@echo ""
	@echo "Visualization:"
	@echo "  make dashboard      Launch Streamlit dashboard"
	@echo ""
	@echo "Cleaning:"
	@echo "  make clean          Remove cache files"
	@echo "  make clean-data     Remove generated datasets"
	@echo ""