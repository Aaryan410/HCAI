from pathlib import Path
import json

BASE_DIR = Path.home() / ".hcai"
HISTORY_DIR = BASE_DIR / "history"


def get_history_path(model_id):
    filename = model_id.replace("/", "_") + ".json"

    return HISTORY_DIR / filename


def load_history(model_id):
    path = get_history_path(model_id)

    if path.exists():
        with open(path, "r", encoding = "utf-8") as f:
            return json.load(f)

    return []


def save_history(model_id, history):
    path = get_history_path(model_id)

    HISTORY_DIR.mkdir(parents = True, exist_ok = True)

    with open(path, "w", encoding = "utf-8") as f:
        json.dump(history, f, indent = 2)