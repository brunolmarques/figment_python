.PHONY: help lint lint-fix test test-cov

# Run ruff linter to check code style and quality
lint:
	ruff check .

# Run ruff linter and automatically fix issues where possible
lint-fix:
	ruff check --fix .

# Run tests
test:
	pytest tests/ -v

# Run tests with coverage report
test-cov:
	pytest tests/ -v --cov=src --cov-report=term-missing

# Default target
help:
	@echo "Available commands:"
	@echo "  make help     - Show this help message"
	@echo "  make lint     - Run ruff linter to check code style and quality"
	@echo "  make lint-fix - Run ruff linter and automatically fix issues where possible"
	@echo "  make test     - Run tests with verbose output"
	@echo "  make test-cov - Run tests with coverage report"


