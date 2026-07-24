from config import save_config, validate_api_key
from models import get_providers, get_models


def main():
    # Starting interface.
    print()

    print('-----------------------------------------------')

    print("\nWelcome to HCAI\n")

    print("Let's get you set up\n")

    print('-----------------------------------------------\n')

    run_setup()


def run_setup():
    # Validate API key.
    while True:
        print("Enter your Hack Club AI key:")
        api_key = input('> ').strip()

        if validate_api_key(api_key):
            print("\n✅ API key validated successfully!")
            break
        else:
            print("\n❌ Invalid API key. Please try again.")


    # Get the provider they want the model from.
    providers = get_providers()

    print("\nAvailable providers")
    print("-------------------\n")

    for i, provider in enumerate(providers, start = 1):
        print(f"{i}. {provider}")

    while True:
        try:
            provider_selected = int(input("Provider number > ").strip())
        except ValueError:
            print("Please enter a number.")
            continue

        if not 1 <= provider_selected <= len(providers):
            print("Invalid choice.")
        else:
            break

    provider = providers[provider_selected - 1]


    # Get the model they want to use.
    models = get_models(provider)

    print("\nType which model you want to use:")
    print("----------------------------------\n")

    for i, model in enumerate(models, start = 1):
        print(f"{i}. {model['name']}")

    while True:
        try:
            model_selected = int(input("Model number > ").strip())
        except ValueError:
            print("Please enter a number.")
            continue

        if not 1 <= model_selected <= len(models):
            print("Invalid choice.")
        else:
            break

    model = models[model_selected - 1]

    print()


    # Save the configured data.
    config_data = {
        "api_key": api_key,
        "provider": provider,
        "model": model["id"]
    }

    save_config(config_data)

    if save_config(config_data):
        print("\n✅ Setup completed succesfully!")
        print("You can now start using HCAI.")
    else:
        print("\n❌ Failed to save configuration.")


if __name__ == "__main__":
    main()