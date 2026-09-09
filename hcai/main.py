from hcai.config import config_exists, load_config, validate_config
from hcai.client import chat
from hcai.history import load_history, save_history
from hcai.setup import run_setup
from hcai.commands import handle_command
from hcai.models import get_model_name
from hcai.ui import render_stream

def print_banner():
    print()
    print("=" * 50)
    print("HCAI v1.0.2")
    print("=" * 50)


def print_model_info(config):
    print(f"Provider : {config['provider']}")
    print(f"Model    : {get_model_name(config['model'])}")
    print()
    print("Type /help for available commands.")
    print("=" * 50)
    print()


def main():
    if not config_exists():

        print()
        print("=" * 50)
        print("Welcome to HCAI!")
        print("=" * 50)
        print()
        print("It looks like this is your first time running HCAI.")
        print("Let's get you set up.")
        print()
        
        run_setup()

    config = load_config()

    if config is None:
        print("❌ Failed to load configuration.")
        raise SystemExit(1)

    if not validate_config(config):
        print("❌ Invalid Configuration")
        raise SystemExit(1)

    print_banner()
    print_model_info(config)

    history = load_history(config["model"])

    try:
        while True:
            prompt = input("HCAI > ").strip()

            if not prompt:
                continue

            if prompt.startswith("/"):
                handled = handle_command(prompt, config, history)

                if handled == "exit":
                    break

                if handled:
                    continue

            answer = render_stream(chat(prompt, history))

            if answer:
                save_history(config["model"], history)

    except KeyboardInterrupt:
        print()
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
