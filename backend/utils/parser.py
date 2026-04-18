import json

def parse_json(output: str):
    try:
        return json.loads(output)
    except (json.JSONDecodeError, ValueError):
        # fallback if LLM adds text
        start = output.find("{")
        end = output.rfind("}") + 1
        return json.loads(output[start:end])