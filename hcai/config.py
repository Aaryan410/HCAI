from pathlib import Path
import json
import keyring

from hcai.models import provider_exists, model_id_exists


CONFIG_PATH = Path.home() / ".hcai" / "config.json"

KEYRING_SERVICE = "hcai"
KEYRING_USERNAME = "api_key"

def get_config_path() -> Path:
    return CONFIG_PATH


def config_exists() -> bool:
    return CONFIG_PATH.is_file()


def validate_api_key(api_key: str) -> bool:
    if not isinstance(api_key, str):
        return False

    return api_key.startswith("sk-hc-v1-")

    
def save_config(config_data: dict) -> bool:
    config_path = get_config_path()

    api_key = config_data.get("api_key")

    disk_data = {k: v for k, v in config_data.items() if k != "api_key"}

    try:
        config_path.parent.mkdir(
            parents = True, 
            exist_ok = True
        )

        with config_path.open("w", encoding = "utf-8") as file:
            json.dump(disk_data, file, indent = 4)
    
    except OSError as e:
        print(f"❌ Failed to save configuration:\n{e}")
        return False

    if api_key is not None:
        try:
            keyring.set_password(KEYRING_SERVICE, KEYRING_USERNAME, api_key)
        except keyring.errors.KeyringError as e:
            print(f"❌ Failed to save API key to system keyring:\n{e}")
            return False

    return True


def load_config() -> dict | None:
    try:
        with get_config_path().open("r", encoding = "utf-8") as file:
            config = json.load(file)
    
    except json.JSONDecodeError as e:
        print(f"❌ Configuration file contains invalid JSON:\n{e}")
        return None

    except OSError as e:
        print(f"❌ Failed to read configuration:\n{e}")
        return None

    if not isinstance(config, dict):
        return config

    legacy_api_key = config.pop("api_key", None)

    if legacy_api_key is not None:
        try:
            keyring.set_password(KEYRING_SERVICE, KEYRING_USERNAME, legacy_api_key)
        except keyring.errors.KeyringError:
            pass
        else:
            try:
                with get_config_path().open("w", encoding = "utf-8") as file:
                    json.dump(config, file, indent = 4)
            except OSError:
                pass

    try:
        stored_key = keyring.get_password(KEYRING_SERVICE, KEYRING_USERNAME)
    except keyring.errors.KeyringError:
        stored_key = None

    config["api_key"] = stored_key if stored_key is not None else legacy_api_key

    return config


def validate_config(config: dict) -> bool:
    required_keys = {
        "api_key",
        "provider",
        "model"
    }

    if not isinstance(config, dict):
        return False

    if not required_keys.issubset(config):
            return False

    if not validate_api_key(config["api_key"]):
        return False

    if not provider_exists(config["provider"]):
        return False

    model_id = config["model"]

    if not model_id_exists(config["provider"], model_id):
        return False

    return True
        