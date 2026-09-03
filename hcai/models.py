import json
from pathlib import Path
import requests

BASE_DIR = Path(__file__).parent
MODELS_FILE = BASE_DIR / "data" / "models.json"

def load_models(file_path: Path = MODELS_FILE) -> dict | None:

    if not file_path.exists(): 
        print(f"❌ Error: File '{file_path}' not found.")
        return None

    try:
        with file_path.open("r", encoding = "utf-8") as f:
            return json.load(f)
        
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON:\n{e}")
        return None

    except OSError as e:
        print(f"❌ Failed to read file:\n{e}")
        return None


def get_providers() -> list[str]:

    data = load_models()

    if not data or not isinstance(data, dict):
        return []

    return list(data.keys())


def provider_exists(provider: str) -> bool:
    providers = get_providers()

    return provider in providers


def get_models(provider: str) -> list[dict] | None:

    data = load_models()

    if not data:
        return None

    return data.get(provider)


def model_exists(provider: str, model_name: str) -> bool:
    models = get_models(provider)

    if not models:
        return False

    for model in models:
        if model["name"] == model_name:
            return True

    return False


def model_id_exists(provider: str, model_id: str) -> bool:

    models = get_models(provider)

    if not models:
        return False
    
    for model in models:
        if model["id"] == model_id:
            return True

    return False


def get_model_id(provider: str, model_name: str) -> str | None:

    models = get_models(provider)

    if not models:
        return None

    for model in models:
        if model["name"] == model_name:
            return model["id"]

    return None


def get_model_name(model_id: str) -> str | None:
    data = load_models()

    if not data:
        return None

    for models in data.values():
        for model in models:
            if model["id"] == model_id:
                return model["name"]

    return None


def find_model(query: str) -> list[dict[str, str]]:

    data = load_models()

    if not data:
        return []

    query = query.casefold()
    matches = []

    for provider, models in data.items():
        for model in models:
            if query in model["name"].casefold():
                matches.append(
                    {
                        "provider": provider,
                        "name": model["name"],
                        "id": model["id"]
                    }
                )

    return matches


def sync_models():

    response = requests.get(
        "https://ai.hackclub.com/proxy/v1/models",
        timeout = 10
    )

    response.raise_for_status()

    data = response.json()

    models = {}
    seen_ids = set()

    for model in data["data"]:
        provider = model["id"].split('/')[0]
        name = model["name"]
        model_id = model["id"]

        if model_id in seen_ids:
            continue

        seen_ids.add(model_id)
        
        context_length = model["context_length"]
        input_modalities = model["architecture"]["input_modalities"]
        output_modalities = model["architecture"]["output_modalities"]
        reasoning = model.get("reasoning")
        pricing = model["pricing"]

        model_data = {
            "name": name,
            "id": model_id,
            "context_length": context_length,
            "input_modalities": input_modalities,
            "output_modalities": output_modalities,
            "reasoning": reasoning,
            "pricing": pricing
        }

        models.setdefault(provider, []).append(model_data)

    with MODELS_FILE.open("w", encoding = "utf-8") as f:
        json.dump(models, f, indent = 4)

sync_models()
