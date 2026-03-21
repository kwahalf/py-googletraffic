# Makefile for py-googletraffic

.PHONY: help install install-dev install-test test test-v test-cov clean lint format contributors

help:
	@echo "py-googletraffic Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  install       - Install package"
	@echo "  install-dev   - Install package with dev dependencies"
	@echo "  install-test  - Install package with test dependencies"
	@echo "  test          - Run tests with nose2"
	@echo "  test-v        - Run tests with verbose output"
	@echo "  test-cov      - Run tests with coverage report"
	@echo "  test-pytest   - Run tests with pytest"
	@echo "  clean         - Remove build artifacts and cache files"
	@echo "  lint          - Run code linting"
	@echo "  format        - Format code with black"
	@echo "  contributors  - Update CONTRIBUTORS.md from git history"
	@echo "  docs          - Generate documentation"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

install-test:
	pip install -e ".[test]"

test:
	nose2

test-v:
	nose2 -v

test-cov:
	nose2 --with-coverage --coverage-report term --coverage-report html
	@echo ""
	@echo "Coverage report generated in htmlcov/"

test-pytest:
	pytest --cov=googletraffic --cov-report=html --cov-report=term

test-unit:
	nose2 tests.test_constants tests.test_utils

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf htmlcov/
	rm -rf test-results/
	rm -rf .coverage
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.tif" -delete
	find . -type f -name "*.tiff" -delete

lint:
	flake8 googletraffic/ --max-line-length=100 --ignore=E203,W503

format:
	black googletraffic/ tests/

check:
	black --check googletraffic/ tests/
	flake8 googletraffic/ --max-line-length=100 --ignore=E203,W503

docs:
	@echo "Documentation is in markdown format:"
	@echo "  - README.md"
	@echo "  - INSTALLATION.md"
	@echo "  - QUICKSTART.md"
	@echo "  - WINDOWS.md"
	@echo "  - COLAB.md"
	@echo "  - CONTRIBUTING.md"
	@echo "  - CONTRIBUTORS.md"
	@echo "  - tests/README.md"

contributors:
	python3 scripts/generate_contributors.py
	@echo ""
	@echo "✅ CONTRIBUTORS.md updated!"
	@echo "📝 Remember to commit the changes."
