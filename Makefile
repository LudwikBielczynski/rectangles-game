.PHONY: help install sync run test format lint clean

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies (sync with uv.lock)"
	@echo "  make sync       - Sync dependencies including dev dependencies"
	@echo "  make run        - Run the game"
	@echo "  make test       - Run tests with pytest"
	@echo "  make format     - Format code with black and isort"
	@echo "  make lint       - Check code formatting"
	@echo "  make clean      - Remove build artifacts and cache files"

install:
	uv sync

sync:
	uv sync --dev

run:
	uv run python -m game.main

test:
	uv run pytest

format:
	uv run isort src/
	uv run black src/

lint:
	uv run isort --check-only src/
	uv run black --check src/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
