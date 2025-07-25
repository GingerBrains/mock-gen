import json

def parse_schema(schema_str):
    """
    Parse the schema string (JSON) into a structured dict.
    Supports both simple and detailed field definitions.
    Example input:
        '{"name": "name", "age": {"type": "integer", "min": 18, "max": 99}}'
    Returns:
        {"name": {"type": "name"}, "age": {"type": "integer", "min": 18, "max": 99}}
    """
    try:
        raw = json.loads(schema_str)
    except Exception as e:
        raise ValueError(f"Invalid schema JSON: {e}")
    parsed = {}
    for field, spec in raw.items():
        if isinstance(spec, str):
            parsed[field] = {"type": spec}
        elif isinstance(spec, dict):
            parsed[field] = dict(spec)
        else:
            raise ValueError(f"Invalid schema for field '{field}': {spec}")
    return parsed 