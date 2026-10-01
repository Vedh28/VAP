# pip install -qU langchain langchain-groq
import os
from pathlib import Path

from langchain.agents import create_agent

env_file = Path(__file__).resolve().parent.parent / ".env"
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        name, separator, value = line.partition("=")
        if separator and name.strip() == "GROQ_API_KEY":
            os.environ.setdefault(name.strip(), value.strip().strip("\"'"))

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="groq:openai/gpt-oss-120b",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in Mumbai?"}]}
)
print(result["messages"][-1].content_blocks)
