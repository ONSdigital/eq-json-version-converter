# eq-json-version-converter
This repository has been written to convert [Survey Runner](https://github.com/ONSdigital/eq-survey-runner) schemas from v2 to v3.


N.B Only e-commerce surveys are currently supported. Other surveys may convert, but aren't guaranteed to be valid to the v3 specification.

## Setup

To install, run the following.

```
pyenv install
pip install --upgrade pip setuptools pipenv
pipenv install --dev
```

## Running

Put any v2 schema you want converted into the directory `schemas/to_convert`:

```
make convert-schemas
```

Results of the conversion will appear in schemas/converted


## Testing against validator

If you want to test the results generated in the `schema/converted` folder against eq schema validator (https://github.com/ONSdigital/eq-schema-validator) use the following command

```
make validate-schemas
```