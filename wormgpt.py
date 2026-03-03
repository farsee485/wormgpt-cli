import json
import os
import time
import requests
from langdetect import detect
from colorama import Fore, Style, init

# Initialize colorama for colored text
init(autoreset=True)

CONFIG_FILE = "wormgpt_config.json"

# Load or create config
if not os.path.exists(CONFIG_FILE):
    config = {
        "api_key": "",
        "model": "gpt-4",
        "language": "auto"
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
else:
    with open(CONFIG_FILE) as f:
        config = json.load(f)

# Ask API key if not set
if not config.get("api_key"):
    config["api_key"] = input(Fore.YELLOW + "Enter your OpenRouter API key: " + Style.RESET_ALL)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Typing effect for output
def typing_print(text):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(0.02)
    print()

# Get response from API
def get_response(prompt):
    headers = {"Authorization": f"Bearer {config['api_key']}"}
    data = {
        "model": config["model"],
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        answer = response.json()["choices"][0]["message"]["content"]
        return answer
    except Exception as e:
        return f"Error: {e}"

# Main chat loop
def main():
    print(Fore.CYAN + "=== Welcome to WormGPT CLI ===" + Style.RESET_ALL)
    print("Type 'exit' to quit\n")

    while True:
        prompt = input(Fore.GREEN + "You: " + Style.RESET_ALL)
        if prompt.lower() == "exit":
            print(Fore.CYAN + "Goodbye!" + Style.RESET_ALL)
            break

        # Detect language if auto
        if config["language"] == "auto":
            lang = detect(prompt)
        else:
            lang = config["language"]

        answer = get_response(prompt)
        typing_print(Fore.MAGENTA + f"WormGPT ({lang}): " + Style.RESET_ALL + answer)

if __name__ == "__main__":
    main()