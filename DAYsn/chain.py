from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pathlib import Path
import os
env_file = Path(__file__).resolve().parent.parent / ".env"
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        name, separator, value = line.partition("=")
        if separator and name.strip() == "GROQ_API_KEY":
            os.environ.setdefault(name.strip(), value.strip().strip("\"'"))
llm = ChatGroq (
    model ="qwen/qwen3.8-27b",
    temperature=0
)
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in 5 simple terms."
)
chain = prompt | llm | StrOutputParser()
def explain_topic(topic):
    return chain.invoke({"topic": topic})
print(explain_topic("Docker"))
print(explain_topic("Kubernetes"))
print(explain_topic("Terraform"))