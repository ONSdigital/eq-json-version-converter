def general_conversions(schema):

    general_rules = {
        "update_meta_data_from_validator_to_type": update_meta_data_from_validator_to_type,
        "update_data_version": update_data_version,
    }

    for key in general_rules:
        general_rules[key](schema)


def update_meta_data_from_validator_to_type(schema):
    metadata = schema.get("metadata", [])
    for item in metadata:
        if "validator" in item:
            item["type"] = item["validator"]
            del item["validator"]


def update_data_version(schema):
    data_version = schema.get("data_version")
    if data_version == "0.0.2":
        schema["data_version"] = "0.0.3"
