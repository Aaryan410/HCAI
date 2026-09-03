from pathlib import Path
from hcai.models import load_models
    

def validate_structure(data: dict) -> tuple[bool, list[str]]:

    errors = []

    if not isinstance(data, dict):
        return False, ["Root JSON structure must be an object/dictionary."]

    for provider, models in data.items():
        if not isinstance(models, list): 
            errors.append(f"Provider '{provider}' must contain a list of models.")
            continue

        if not models:
            errors.append(f"Provider '{provider}' has an empty model list.")

        for index, model in enumerate(models): 
            if not isinstance(model, dict):
                errors.append(f"Provider '{provider}' item #{index} is not an object.")
                continue

            name = model.get("name")
            model_id = model.get("id")

            if not isinstance(name, str) or not name.strip():
                errors.append(f"Provider '{provider}' item #{index} has an invalid 'name'.")

            if not isinstance(model_id, str) or not model_id.strip():
                errors.append(f"Provider '{provider}' item #{index} has an invalid 'id'.")

    return len(errors) == 0, errors


def main() -> int:

    data = load_models()

    if data is None:
        return 1

    print("✅ models.json loaded successfully.")

    valid, errors = validate_structure(data)

    if valid:
        print("✅ Structure Validation passed!")
        return 0
    else:
        print("❌ Structure validation failed.\n")

        for error in errors:
            print(f" - {error}")

        return 1

if __name__ == "__main__":
    raise SystemExit(main()) 
