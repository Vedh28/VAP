import os
from pathlib import Path

from groq import Groq


MODEL_NAME = "qwen/qwen3.8-27b"


def load_env_file() -> None:
    env_file = Path(__file__).with_name(".env")
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            name, separator, value = line.partition("=")
            if separator and name.strip() == "GROQ_API_KEY":
                os.environ.setdefault(name.strip(), value.strip().strip("\"'"))


def run_agent() -> None:
    load_env_file()
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise SystemExit("GROQ_API_KEY is missing from the environment and .env file.")

    client = Groq(api_key=api_key)
    messages = [{
        "role": "system",
        "content": "Repeat each user's message exactly, character for character. Do not add, remove, or change anything.",
    }]
    print("Groq assistant — type 'exit' to quit.")
    while True:
        prompt = input("\nYou: ").strip()
        if prompt.lower() == "exit":
            break
        if prompt:
            messages.append({"role": "user", "content": prompt})
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0,
            )
            reply = response.choices[0].message.content or ""
            messages.append({"role": "assistant", "content": reply})
            print("Assistant:", reply)


if __name__ == "__main__":
    run_agent()
