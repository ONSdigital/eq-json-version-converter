# Some metadata needs to be substituted from v2 to v3 as it can no longer be used in its current format
# or has been deprecated like the '_or_' operator

metadata_substitutions = [
    {
        'metadata_name': 'trad_as_or_runame',
        'type': 'transforms',
        'placeholder_name': 'company_name',
        'transform': 'first_non_empty_item',
        'identifier': ['trad_as', 'ru_name'],
    }
]
