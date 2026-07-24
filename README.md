# HCAI

A lightweight AI command-line interface powered by Hack Club AI.

HCAI allows you to chat with multiple AI models directly from your terminal with streaming responses, persistent conversation history, and seamless model switching.

---

## Features

- 🚀 Real-time streaming responses
- 🤖 Multiple AI providers
- 💬 Persistent conversation history
- 🔄 Switch models anytime
- ⚙️ Interactive first-time setup
- 📁 Configuration stored automatically
- 🧹 Clear conversation history
- 💻 Lightweight terminal interface

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/HCAI.git
```

Move into the project

```bash
cd HCAI
```

Install

```bash
py -m pip install -e .
```

---

## First Launch

Simply run

```bash
hcai
```

On the first launch HCAI will ask for

- Hack Club AI API Key
- Provider
- Model

The configuration is automatically saved.

---

## Usage

Start HCAI

```bash
hcai
```

Example

```text
> Explain recursion.

Recursion is a programming technique...
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/use` | Switch models interactively |
| `/use <query>` | Search and switch models |
| `/config` | Show current configuration |
| `/clear` | Clear current conversation |
| `/exit` | Exit HCAI |

Examples

```text
/use claude
/use gemini
/use gpt
/use opus
```

---

## Project Structure

```
HCAI/
│
├── hcai/
│   ├── client.py
│   ├── commands.py
│   ├── config.py
│   ├── history.py
│   ├── main.py
│   ├── models.py
│   ├── setup.py
│   └── data/
│       └── models.json
│
├── pyproject.toml
├── README.md
└── requirements.txt
```

---

## Tech Stack

- Python
- Requests
- JSON
- Hack Club AI API

---

## License

MIT License


## Credit:
- I used ChatGPT for guidance to make it, for fixing bugs and errors like for example how would I publish it on PyPI, if i get an Error how to handle it and make it more user friendly etc. I wrote the most of the code myself.
