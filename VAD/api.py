import os
from pathlib import Path

from groq import Groq


env_file = Path(__file__).with_name(".env")
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        name, separator, value = line.partition("=")
        if separator and name.strip() == "GROQ_API_KEY":
            os.environ.setdefault(name.strip(), value.strip().strip("\"'"))

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise SystemExit("GROQ_API_KEY is missing from the environment and .env file.")

client = Groq(api_key=api_key)
print("=== YOUR ACTIVE GROQ MODELS ===")
for model in client.models.list().data:
    print(f"- {model.id}")
