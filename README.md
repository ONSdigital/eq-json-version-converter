# eq-json-version-converter
This repository has been written to convert v2 Survey Runner JSON (https://github.com/ONSdigital/eq-survey-runner) to v3.

N.B This was written for the e-commerce survey, so although it might convert some other v2 surveys they might not pass validation.

## Setup

This application uses pipenv, please follow the following steps.

```
pyenv install
pip install --upgrade pip setuptools pipenv
pipenv install --dev
pipenv shell
```

## Running

To use the application, first populate the directory  `schemas/to_convert` with your v2 Survey Runner JSON then run:

```
pipenv run python app.py
```

Results of the conversion will appear in schemas/converted


## Testing against validator

If you want to test the results generated in the `schema/converted` folder against eq schema validator (https://github.com/ONSdigital/eq-schema-validator) use the following command

```
pipenv run ./scripts/test_schemas_against_validator.sh
```