.PHONY: help install install-dev clean lint format test coverage build publish-test publish

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development

install: ## Install the package
	python -m pip install -e .

install-dev: ## Install the package and development dependencies
	python -m pip install -e ".[test]"

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.cover" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

##@ Code Quality

lint: ## Run linting (ruff + mypy)
	ruff check .
	mypy mcp_jetbrains_proxy tests

format: ## Format code (ruff)
	ruff format .

##@ Testing

test: ## Run tests
	pytest

coverage: ## Run tests with coverage report
	pytest --cov=mcp_jetbrains_proxy --cov-report=term-missing --cov-report=html

##@ Build and Publish

build: clean ## Build package
	python -m build

publish-test: build ## Publish to TestPyPI
	python -m twine upload --repository testpypi dist/*

publish: build ## Publish to PyPI
	python -m twine upload dist/*
