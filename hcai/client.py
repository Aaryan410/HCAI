import requests
import json
from hcai.config import load_config, validate_config


API_URL = "https://ai.hackclub.com/proxy/v1/chat/completions"
TIMEOUT = 60


def create_headers(api_key: str) -> dict[str, str]:

    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }   


def create_payload(model: str, messages: list[dict], stream: bool = True) -> dict:

    payload = {
        "model": model,
        "messages": messages,
    }

    if stream:
        payload["stream"] = True

    return payload


def send_message(messages: list[dict[str, str]]) -> requests.Response | None:
    config = load_config()

    if not config:
        print("❌ Failed to load configuration.")
        return None

    if not validate_config(config):
        print("❌ Invalid configuration.")
        return None

    api_key = config.get("api_key")
    model = config.get("model")

    headers = create_headers(api_key)

    payload = create_payload(model, messages)

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            stream=True,
            timeout=TIMEOUT
        )

        response.raise_for_status()
        return response

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response else None

        if status == 401:
            print("\n❌ Invalid API key.")
            print("Please check your API key and try again.\n")

        elif status == 403:
            print("\n❌ Access denied.")
            print("Your API key doesn't have permission to access this resource.\n")

        elif status == 404:
            print("\n❌ Model or endpoint not found.\n")

        elif status == 429:
            print("\n❌ Rate limit exceeded.")
            print("Please wait a moment and try again.\n")

        elif status == 500:
            print("\n❌ Internal server error.")
            print("Please try again later.\n")

        elif status == 502:
            print("\n❌ Bad gateway.")
            print("The AI provider is temporarily unavailable.\n")

        elif status == 503:
            print("\n❌ Service unavailable.")
            print("Please try again later.\n")

        elif status == 504:
            print("\n❌ The AI server took too long to respond.")
            print("This is usually temporary.")
            print("Try sending the message again or switch to another model with /use.\n")

        else:
            print(f"\n❌ HTTP Error {status}")

            if e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"Details: {error_data}")
                except ValueError:
                    print(f"Details: {e.response.text}")

            print()

    except requests.exceptions.Timeout:
        print("\n❌ The request timed out.")
        print("Please try again.\n")

    except requests.exceptions.ConnectionError:
        print("\n❌ Unable to connect to the AI server.")
        print("Please check your internet connection.\n")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed:\n{e}")

    return None


def stream_response(response: requests.Response) -> str:

    full_response = ""

    try:
        for line in response.iter_lines():

            if not line:
                continue

            line = line.decode("utf-8")

            if not line.startswith("data: "):
                continue
            
            if line == "data: [DONE]":
                break

            try:
                data = json.loads(line[6:])

                choice = data["choices"][0]

                delta = choice.get("delta") or {}

                content = delta.get("content", "")

                if content:
                    print(content, end = "", flush = True)
                    full_response += content

            except (json.JSONDecodeError, KeyError, IndexError):
                continue

    except requests.exception.RequestException as e:
        print(f"\n❌ The response stream was interrupted:\n{e}")

    print()
    return full_response


def chat(prompt: str, messages: list[dict]) -> str | None:

    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    response = send_message(messages)

    if response is None: 
        return None

    answer = stream_response(response)

    if not answer:
        print("❌ The AI returned an empty response.")
        return None

    messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    return answer
