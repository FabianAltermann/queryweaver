all: install check tests

.PHONY: install
install:
	uv sync

.PHONY: check
check: lint format

.PHONY: lint
lint:
	uv run ruff check --fix

.PHONY: typecheck
typecheck:
	uv run mypy .

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

.PHONY: project-version
.SILENT: project-version
project-version:
	uv run --no-project ./tools/version.py --version

.PHONY: project-info
.SILENT: project-info
project-info:
	uv run --no-project ./tools/version.py --info

.PHONY: project-name
.SILENT: project-name
project-name:
	uv run --no-project ./tools/version.py --name
