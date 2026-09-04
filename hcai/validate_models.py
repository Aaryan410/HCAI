from pathlib import Path
from hcai.models import load_models
    

def validate_structure(data: dict) -> tuple[bool, list[str]]:

    errors = []
    seen_ids = set()

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

            context_length = model.get("context_length")
            input_modalities = model.get("input_modalities")
            output_modalities = model.get("output_modalities")
            reasoning = model.get("reasoning")
            pricing = model.get("pricing")

            # name
            if not isinstance(name, str) or not name.strip():
                errors.append(f"Provider '{provider}' item #{index} has an invalid 'name'.")

            # model id
            if not isinstance(model_id, str) or not model_id.strip():
                errors.append(f"Provider '{provider}' item #{index} has an invalid 'id'.")
            else:
                if model_id in seen_ids:
                    errors.append(f"Provider '{provider}' item #{index} has a duplicate model ID: '{model_id}'.")
                else:
                    seen_ids.add(model_id)  

            # context length
            if not isinstance(context_length, int) or not context_length:
                errors.append(f"Provider '{provider}' item #{index} has an invalid 'context length'.")

            # input modalities
            if not isinstance(input_modalities, list) or not input_modalities:
                errors.append(f"Provider '{provider}' item #{index} has an invalid 'input modalities'.")

            if isinstance(input_modalities, list):
                if not all(isinstance(modality, str) for modality in input_modalities):
                    errors.append(f"Provider '{provider}' item #{index} has invalid values in 'input modalities'.")

            # output modalities
            if isinstance(output_modalities, list):
                if not all(isinstance(modality, str) for modality in output_modalities):
                    errors.append(f"Provider '{provider}' item #{index} has invalid values in 'output modalities'.")

            if not isinstance(output_modalities, list) or not output_modalities:
                errors.append(f"Provider '{provider}' item #{index} has an invalid 'output modalities'.")

            # reasoning 
            if reasoning is not None and not isinstance(reasoning, dict):
                errors.append(f"Provider '{provider}' item #{index} has an invalid 'reasoning'.")

            if isinstance(reasoning, dict):
                if "mandatory" in reasoning and not isinstance(reasoning["mandatory"], bool):
                    errors.append(f"Provider '{provider}' item #{index} has an invalid 'reasoning.mandatory'.")

                if "default_enabled" in reasoning and not isinstance(reasoning["default_enabled"], bool):
                    errors.append(f"Provider '{provider}' item #{index} has an invalid 'reasoning.default_enabled'.")

                if "supported_efforts" in reasoning:
                    if not isinstance(reasoning["supported_efforts"], list) or not reasoning["supported_efforts"]:
                        errors.append(f"Provider '{provider}' item #{index} has an invalid 'reasoning.supported_efforts'.")
                    elif not all(isinstance(effort, str) for effort in reasoning["supported_efforts"]):
                        errors.append(f"Provider '{provider}' item #{index} has an invalid values in 'reasoning.supported_efforts'")

                if "default_effort" in reasoning and not isinstance(reasoning["default_effort"], str):
                    errors.append(f"Provider '{provider}' item #{index} has an invalid 'reasoning.default_effort'.")

                if "supports_max_tokens" in reasoning and not isinstance(reasoning["supports_max_tokens"], bool):
                    errors.append(f"Provider '{provider}' item #{index} has an invalid 'reasoning.supports_max_tokens'.")

            # pricing
            if not isinstance(pricing, dict):
                errors.append(f"Provider '{provider}' item #{index} has an invalid 'pricing'.")

            if isinstance(pricing, dict):
                for key, value in pricing.items():
                    if key == "overrides":
                        if not isinstance(value, list):
                            errors.append(f"Provider '{provider}' item #{index} has invalid 'pricing.overrides'.")

                    elif not isinstance(value, str):
                        errors.append(f"Provider '{provider}' item #{index} has invalid pricing value for '{key}'.")

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
