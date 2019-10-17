convert-schemas:
	pipenv run python app.py

validate-schemas:
	pipenv run ./scripts/test_schemas_against_validator.sh

lint:
	pipenv run ./scripts/run_lint.sh