.PHONY: clean format build publish install help

PYTHON := uv python
PIP := uv pip

help:
	@echo "Available commands:"
	@echo "  make clean      - Remove build artifacts"
	@echo "  make format     - Format code using black"
	@echo "  make build      - Build package"
	@echo "  make publish    - Publish package to PyPI"
	@echo "  make install    - Install development dependencies"

clean:
	rm -rf dist/ build/ *.egg-info/

format:
	uv run black src/wox_plugin

build: install clean format
	uv run hatchling build

publish: build
	uv run twine upload dist/*

install:
	uv sync --all-extras
