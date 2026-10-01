import os
from pathlib import Path

from langchain_groq import ChatGroq

env_file = Path(__file__).resolve().parent.parent / ".env"
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        name, separator, value = line.partition("=")
        if separator and name.strip() == "GROQ_API_KEY":
            os.environ.setdefault(name.strip(), value.strip().strip("\"'"))

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
response = llm.invoke(
    "Explain Docker in simple terms."
)
print(response.content)
