from pathlib import Path
import json

from hcai.models import provider_exists, model_id_exists


CONFIG_PATH = Path.home() / ".hcai" / "config.json"

def get_config_path() -> Path:
    """
    Return the path to the HCAI configuration file.
    """
    return CONFIG_PATH



def config_exists() -> bool:
    """
    Check whether the configuration file exists.
    """
    return CONFIG_PATH.is_file()



def validate_api_key(api_key: str) -> bool:
    """
    Validate a Hack Club AI API key.
    """
    return api_key.startswith("sk-hc-v1-")


    
def save_config(config_data: dict) -> None:
    """
    Save the configuration to the disk

    Returns:
        True if succesful.
        False otherwise
    """

    config_path = get_config_path()

    try:
        config_path.parent.mkdir(
            parents = True, 
            exist_ok = True
        )

        with config_path.open("w", encoding = "utf-8") as file:
            json.dump(config_data, file, indent = 4)
    
        return True
    
    except OSError as e:
        print(f"❌ Failed to save configuration:\n{e}")
        return False



def load_config() -> dict | None:
    """
    Load the configuration from disk.
    """

    try:
        with get_config_path().open("r", encoding = "utf-8") as file:
            return json.load(file)
    
    except json.JSONDecodeError as e:
        print(f"❌ Configuration file not  found:\n{e}")
        return None

    except OSError as e:
        print(f"❌ Failed to read configuration:\n{e}")
        return None


def validate_config(config: dict) -> bool:
    """
    Validate the configuration dictionary.
    """ 


    required_keys = {
        "api_key",
        "provider",
        "model"
    }

    if not required_keys.issubset(config):
        return False

    if not validate_api_key(config["api_key"]):
        return False

    if not provider_exists(config["provider"]):
        return False

    model_name = config["model"]

    if not model_id_exists(config["provider"], model_name):
        return False

    return True
        