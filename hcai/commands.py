from hcai.models import(get_providers, get_models, find_model, get_model_name)
from hcai.config import save_config
from hcai.history import load_history, save_history


def handle_command(prompt, config, history):

    command = prompt.split()[0].lower()

    if command == "/help":
        return cmd_help()

    elif command == "/exit":
        return cmd_exit()

    elif command == "/use":
        return cmd_use(prompt, config, history)

    elif command == "/config":
        return cmd_config(config, history)

    elif command == "/clear":
        return cmd_clear(config, history)

    return False


def cmd_exit():

    print("\n👋 Goodbye!")

    return "exit"


def cmd_use(prompt: str, config: dict, history: list) -> bool:
    
    parts = prompt.split(maxsplit=1)

    # ==========================
    # Interactive mode (/use)
    # ==========================
    if len(parts) == 1:

        providers = get_providers()

        print("\nAvailable Providers\n")

        for i, provider in enumerate(providers, start=1):
            print(f"{i}. {provider}")

        while True:
            try:
                choice = int(input("\nProvider number > "))

                if 1 <= choice <= len(providers):
                    break

                print("Invalid choice.")

            except ValueError:
                print("Please enter a number.")

        provider = providers[choice - 1]
        models = get_models(provider)

        print(f"\n{provider} Models\n")

        for i, model in enumerate(models, start=1):
            print(f"{i}. {model['name']}")

        while True:
            try:
                choice = int(input("\nModel number > "))

                if 1 <= choice <= len(models):
                    break

                print("Invalid choice.")

            except ValueError:
                print("Please enter a number.")

        model = models[choice - 1]

        return switch_model(config, history, provider, model)

    # ==========================
    # Search mode (/use claude)
    # ==========================
    query = parts[1]

    matches = find_model(query)

    if not matches:
        print("No matching models found.")
        return True

    if len(matches) == 1:
        match = matches[0]

        model = {
            "name": match["name"],
            "id": match["id"]
        }

        return switch_model(
            config,
            history,
            match["provider"],
            model
        )

    print()

    for i, match in enumerate(matches, start=1):
        print(f"{i}. {match['name']} ({match['provider']})")

    while True:
        try:
            choice = int(input("\nModel number > "))

            if 1 <= choice <= len(matches):
                break

            print("Invalid choice.")

        except ValueError:
            print("Please enter a number.")

    match = matches[choice - 1]

    model = {
        "name": match["name"],
        "id": match["id"]
    }

    return switch_model(
        config,
        history,
        match["provider"],
        model
    )
 

def switch_model(config, history, provider, model):

    config["provider"] = provider
    config["model"] = model["id"]

    if not save_config(config):
        return False

    history.clear()
    history.extend(load_history(model["id"]))

    print(f"\n✓ Switched to {model['name']}")

    return True


def cmd_config(config, history):

    print()

    print("Current Configuration")
    print("---------------------")
    print(f"Provider : {config['provider']}")
    print(f"Model    : {get_model_name(config['model'])}")
    print(f"ID       : {config['model']}")
    print(f"History  : {len(history)} messages")
    print()

    return True


def cmd_clear(config, history):

    history.clear()

    save_history(config["model"], history)

    print("\n✓ Conversation cleared.\n")

    return True


def cmd_help():

    print()

    print("Available Commands")
    print("------------------")
    print("/help      Show this help.")
    print("/use       Switch AI model.")
    print("/config    Show current configuration.")
    print("/clear     Clear current conversation.")
    print("/exit      Exit HCAI.")
    print()

    return True