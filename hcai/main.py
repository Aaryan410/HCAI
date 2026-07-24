from hcai.config import config_exists, load_config
from hcai.client import chat
from hcai.history import load_history, save_history
from hcai.setup import run_setup
from hcai.commands import handle_command
from hcai.models import get_model_name

def main():
    if not config_exists():
        run_setup()

    config = load_config()

    print()
    print("=" * 50)
    print("HCAI v1.0")
    print("=" * 50)
    print(f"Provider : {config['provider']}")
    print(f"Model    : {get_model_name(config['model'])}")
    print()
    print("Type /help for available commands.")
    print("=" * 50)
    print()

    if config is None:
        print("❌ Failed to load configuration.")
        exit(1)

    history = load_history(config["model"])

    while True:
        prompt = input("> ").strip()

        if not prompt:
            continue

        if prompt.startswith("/"):
            handled = handle_command(prompt, config, history)

            if handled == "exit":
                break

            if handled:
                continue

        answer = chat(prompt, history)

        if answer is not None:
            save_history(config["model"], history)

if __name__ == "__main__":
    main()