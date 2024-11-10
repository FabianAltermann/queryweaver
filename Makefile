all: install check tests

.PHONY: install
install:
	uv sync

.PHONY: check
check: lint format

.PHONY: lint
lint:
	uv run ruff check --fix

.PHONY: format
format:
	uv run ruff format

.PHONY: tests
tests:
	uv run coverage run
	uv run coverage report
	uv run coverage html

.PHONY: build
build:
	uv build

.PHONY: clean
clean:
	rm -rf dist
	rm -rf reports


.PHONY: docs
docs:
	uv run mkdocs gh-deploy
