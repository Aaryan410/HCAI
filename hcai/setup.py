from config import save_config

print()

print('-----------------------------------------------')

print("\nWelcome to HCAI\n")

print("Let's get you set up\n")

print('-----------------------------------------------\n')

print("Enter your Hack Club AI key:")
api_key = input('> ').strip()

print("\nAvailable providers\n")

print("Anthropic")
print("Google")
print("OpenAI")
print("Qwen")
print("DeepSeek")
print("xAI")

print("\nType provider name:")
provider = input('> ').strip

print("\nType which model you want to use:")
model = input('> ').strip()

print()

config_data = {
    "api_key": api_key,
    "provider": provider,
    "model": model
}

save_config(config_data)