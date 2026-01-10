import json
import re
import requests

MODEL_URL = "http://localhost:11434/api/generate"


def call_ai(prompt: str):
    body = {
        "model": "llama3.1:8b",
        "prompt": prompt,
        "stream": False,
        "temperature": 0,
    }

    res = requests.post(MODEL_URL, json=body)
    return res.json().get("response", "")


def extract_json(raw: str):
    match = re.search(r"\{[\s\S]*\}", raw)
    if not match:
        return {"error": "JSON not found", "raw": raw}

    try:
        return json.loads(match.group(0))
    except Exception as e:
        return {
            "error": "Invalid JSON",
            "details": str(e),
            "raw_json": match.group(0),
        }


def get_services():
    return {
        "call_ai": call_ai,
        "extract_json": extract_json,
    }
