.PHONY: clean build publish install help

PYTHON := uv python
PIP := uv pip

help:
	@echo "Available commands:"
	@echo "  make clean      - Remove build artifacts"
	@echo "  make build      - Build package"
	@echo "  make publish    - Publish package to PyPI"
	@echo "  make install    - Install development dependencies"
	@echo "  make lint       - Run linting"
	@echo "  make format     - Run formatting"

clean:
	rm -rf dist/ build/ *.egg-info/

install:
	uv sync --all-extras

lint:
	uv run ruff check .

format:
	uv run ruff format .

build: install clean lint format
	uv run hatchling build

publish: build
	uv run twine upload dist/*
