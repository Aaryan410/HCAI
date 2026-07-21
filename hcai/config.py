from pathlib import Path
import json

def get_config_path():
    return Path.home() / ".hcai" / "config.json"

def config_exists():
    return get_config_path().is_file()

def validate_api_key(api_key: str) -> bool:
    if api_key.startswith("sk-hc-v1-"):
        return True
    else:
        return False
    
def save_config(config_data: dict):
    config_path = get_config_path()

    config_path.parent.mkdir(parents = True, exist_ok = True)

    with open(config_path, "w") as file:
        json.dump(config_data, file, indent = 4)


def load_config():
    with open(get_config_path(), "r") as file:
        return json.load(file)

        