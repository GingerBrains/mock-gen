import json

def write_json(data, output_file=None):
    """Write data to JSON format. If output_file is None, print to stdout."""
    json_str = json.dumps(data, indent=2)
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json_str)
    else:
        print(json_str) 