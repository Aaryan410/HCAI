import requests
import json
from hcai.config import load_config


API_URL = "https://ai.hackclub.com/proxy/v1/chat/completions"

def create_headers(api_key: str) -> dict[str, str]:
    """
    Create the HTTP headers for a HACk CLUB AI request.
    """

    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }   


def create_payload(model: str, messages: list[dict], stream: bool = True) -> dict:
    """
    Create the JSON payload for a HACK CLUB AI request.
    """

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

    api_key = config.get("api_key")
    model = config.get("model")

    headers = create_headers(api_key)

    payload = create_payload(model, messages)

    TIMEOUT = 60

    try:
        response = requests.post(
            API_URL,
            headers = headers,
            json = payload,
            stream = True,
            timeout = TIMEOUT
        )

        response.raise_for_status()

        return response
    except requests.RequestException as e:
        print(f"❌ Request failed:\n{e}")
        return None


def stream_response(response: requests.Response) -> str:
    """
    Stream the AI response and return the complete text.
    """

    full_response = ""

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

    print()

    return full_response


def chat(prompt: str, messages: list[dict]) -> str | None:
    """
    Send a prompt to the AI and update the conversation history.
    """    

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

    messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    return answer
