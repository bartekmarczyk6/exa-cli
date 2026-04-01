import os
import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".exa"
CONFIG_FILE = CONFIG_DIR / "config.json"

def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_config(config_data):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=2)

def get_api_key(api_key_override=None):
    if api_key_override:
        return api_key_override
    if "EXA_API_KEY" in os.environ:
        return os.environ["EXA_API_KEY"]
    config = load_config()
    return config.get("api_key")

def get_default(key, default=None):
    config = load_config()
    return config.get(key, default)
