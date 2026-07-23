import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
MODELS_FILE = BASE_DIR / "data" / "models.json"

def load_models(file_path: Path = MODELS_FILE) -> dict | None:
    """Load models.json file and return the parsed data."""

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
    """
    Check if a provider exists in models.json.
    """
    providers = get_providers()

    return provider in providers


def get_models(provider: str) -> list[dict] | None:
    """
    Return all models for a provider.
    """

    data = load_models()

    if not data:
        return None

    return data.get(provider)


def model_exists(provider: str, model_name: str) -> bool:
    """
    Check whether a model exists for a provider.
    """
    models = get_models(provider)

    if not models:
        return False

    for model in models:
        if model["name"] == model_name:
            return True

    return False


def model_id_exists(provider: str, model_id: str) -> bool:
    """
    Check whether a model ID exists for a provider.
    """

    models = get_models(provider)

    if not models:
        return False
    
    for model in models:
        if model["id"] == model_id:
            return True

    return False


def get_model_id(provider: str, model_name: str) -> str | None:
    """
    Return the model ID for a given provider and model name.
    """

    models = get_models(provider)

    if not models:
        return None

    for model in models:
        if model["name"] == model_name:
            return model["id"]

    return None


def get_model_name(model_id: str) -> str | None:
    """
    Return the display name for a model ID.
    """
    data = load_models()

    if not data:
        return None

    for models in data.values():
        for model in models:
            if model["id"] == model_id:
                return model["name"]

    return None


def find_model(query: str) -> list[dict[str, str]]:
    """
    Search for models by name (case-insensitive)

    Returns a list of matching models.
    """

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
