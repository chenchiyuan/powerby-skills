#!/usr/bin/env python3
"""Validate design language extraction output against schema.json."""

import json
import sys
from pathlib import Path

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


def validate(output_path: str, schema_path: str | None = None) -> dict:
    """Validate output JSON against schema. Returns {valid, errors, warnings}."""
    if schema_path is None:
        schema_path = str(
            Path(__file__).resolve().parent.parent / "schemas" / "schema.json"
        )

    with open(schema_path) as f:
        schema = json.load(f)
    with open(output_path) as f:
        data = json.load(f)

    result = {"valid": True, "errors": [], "warnings": []}

    # Structural validation via jsonschema if available
    if HAS_JSONSCHEMA:
        validator = jsonschema.Draft202012Validator(schema)
        for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
            result["errors"].append(
                f"{'.'.join(str(p) for p in error.path) or '(root)'}: {error.message}"
            )
        if result["errors"]:
            result["valid"] = False
    else:
        # Fallback: check top-level required keys
        required = schema.get("required", [])
        for key in required:
            if key not in data:
                result["errors"].append(f"Missing required top-level field: {key}")
                result["valid"] = False

    # Coverage warnings
    tokens = data.get("tokens", {})
    if not tokens.get("alias"):
        result["warnings"].append("Alias tokens missing — components cannot consume tokens")
    if not data.get("evidence"):
        result["warnings"].append("Evidence array is empty — no traceability")
    if not data.get("components"):
        result["warnings"].append("Components array is empty")
    if not data.get("patterns"):
        result["warnings"].append("Patterns array is empty")

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_output.py <output.json> [schema.json]")
        sys.exit(1)

    output_file = sys.argv[1]
    schema_file = sys.argv[2] if len(sys.argv) > 2 else None
    result = validate(output_file, schema_file)

    if result["errors"]:
        print(f"ERRORS ({len(result['errors'])}):")
        for e in result["errors"]:
            print(f"  - {e}")
    if result["warnings"]:
        print(f"\nWARNINGS ({len(result['warnings'])}):")
        for w in result["warnings"]:
            print(f"  - {w}")
    if result["valid"] and not result["warnings"]:
        print("VALID: Output passes schema validation with no warnings.")
    elif result["valid"]:
        print(f"\nVALID with {len(result['warnings'])} warning(s).")
    else:
        print(f"\nINVALID: {len(result['errors'])} error(s) found.")
        sys.exit(1)
