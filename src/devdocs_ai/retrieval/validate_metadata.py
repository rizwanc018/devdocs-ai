def validate_metadata(
    extracted_metadata: dict,
    catalog: dict,
) -> dict:
    if not isinstance(extracted_metadata, dict):
        raise TypeError("Extracted metadata must be a dictionary.")

    validated_metadata = {}

    for field, values in extracted_metadata.items():
        if field not in catalog:
            continue

        if not isinstance(values, list):
            continue

        valid_values = (
            [
                value
                for value in values
                if type(value) is type(catalog[field][0]) and value in catalog[field]
            ]
            if catalog[field]
            else []
        )

        if valid_values:
            validated_metadata[field] = list(dict.fromkeys(valid_values))

    return validated_metadata
