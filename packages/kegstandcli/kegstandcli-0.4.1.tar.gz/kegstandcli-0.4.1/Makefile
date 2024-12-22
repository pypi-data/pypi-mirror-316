now := $(shell date -u '+%Y%m%d-%H%M')

#* Install
.PHONY: install
install:
	uv sync

#* Clean
.PHONY: clean
clean:
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .uv
	rm -rf dist
	rm src/kegstandcli/cdk.context.json
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +

#* Format
.PHONY: lint-fix
lint-fix:
	uv run ruff format
	uv run ruff check --fix

#* Lint
.PHONY: lint-check
lint-check:
	uv run ruff check

.PHONY: lint-types
lint-types:
	uv run mypy --config-file pyproject.toml src tests

.PHONY: lint
lint: lint-check lint-types

#* Poetry (used for unit testing)
.PHONY: poetry-download
poetry-download:
	curl -sSL https://install.python-poetry.org | $(PYTHON) -

#* Test
.PHONY: test
test:
	uv run pytest -c pyproject.toml --cov-report=term --cov=src tests

#* E2E Test
.PHONY: e2e
e2e:
	@echo "Running E2E tests"
	@rm -rf .temp
	@mkdir -p .temp
	@echo "Creating a new project in kegstand-test-$(now)..."
	@cd .temp && uv run keg new --data-file ../tests/test_data/e2e-uv.yaml kegstand-test-$(now)
	@echo "Building..."
	@cd .temp/kegstand-test-$(now) && uv run keg build
	@echo "Deploying..."
	@cd .temp/kegstand-test-$(now) && uv run keg deploy
