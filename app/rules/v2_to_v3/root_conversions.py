from app.metadata_substitutions import metadata_substitutions


def root_conversions(schema):

    general_rules = {
        'update_meta_data_from_validator_to_type': update_meta_data_from_validator_to_type,
        'remove_unused_metadata': remove_unused_metadata,
        'update_data_version': update_data_version,
    }

    for key in general_rules:
        general_rules[key](schema)


def update_meta_data_from_validator_to_type(schema):

    for item in schema.get('metadata', []):
        if 'validator' in item:
            item['type'] = item['validator']
            del item['validator']


def remove_unused_metadata(schema):
    for item in schema.get('metadata', []):
        for replacement in metadata_substitutions:
            if item['name'] == replacement.get('metadata_name'):
                schema.get('metadata').remove(item)


def update_data_version(schema):
    data_version = schema.get('data_version')
    if data_version == '0.0.2':
        schema['data_version'] = '0.0.3'
