"""Helper to safely parse JSON out of an LLM text response."""
import json
import re


def extract_json(text: str) -> dict:
    """
    Extracts the first JSON object found in a string, stripping markdown
    code fences (```json ... ```) if present. Returns {} on failure.
    """
    if not text:
        return {}

    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned.strip(), flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"```$", "", cleaned.strip()).strip()

    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        return {}

    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return {}
