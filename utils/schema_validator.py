import json
import os
from jsonschema import validate, ValidationError


def validate_response(response_json, schema_name):
    """Validate a JSON response against a schema file in the schemas/ directory."""
    schema_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "schemas", f"{schema_name}.json"
    )
    with open(schema_path) as f:
        schema = json.load(f)
    validate(instance=response_json, schema=schema)
