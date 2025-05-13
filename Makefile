.PHONY: help lint lint-fix test test-cov

# Run ruff linter to check code style and quality
lint:
	ruff check .

# Run ruff linter and automatically fix issues where possible
lint-fix:
	ruff check --fix .

# Run the main script
run:
	python3 -m src.main

# Run tests
test:
	pytest tests/ -v

# Run tests with coverage report
test-cov:
	pytest tests/ -v --cov=src --cov-report=term-missing

# Run the display_data.py script
show-data:
	python3 -m scripts.display_data

# Default target
help:
	@echo "Available commands:"
	@echo "  make help     - Show this help message"
	@echo "  make lint     - Run ruff linter to check code style and quality"
	@echo "  make lint-fix - Run ruff linter and automatically fix issues where possible"
	@echo "  make test     - Run tests with verbose output"
	@echo "  make test-cov - Run tests with coverage report"
	@echo "  make run      - Run the main script"
