.PHONY: requirements-dev build run format deps deps-dev test coverage


requirements-dev:
	@poetry export -f requirements.txt -o requirements.txt --with dev


build:
	@$(MAKE) requirements-dev
	@docker build -t favoriteproduct .
	@rm -f requirements.txt

run:
	@if [ ! -f .env ]; then \
		echo "Create env file .env..."; \
		cp -f .env.default .env; \
	fi
	@$(MAKE) build
	@docker compose up -d

format:
	@poetry run pre-commit run --all-files

test:
	@ENVIRONMENT="testing" DB_URL="mongodb://user:pass@localhost/ffavoriteproduct_test?authSource=admin"
	@poetry run coverage run -m pytest

coverage:
	@poetry run coverage report
