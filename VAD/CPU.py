import json
import os
import platform
from pathlib import Path

import psutil
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition


def load_env_file() -> None:
    env_file = Path(__file__).resolve().parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            name, separator, value = line.partition("=")
            if separator and name.strip() == "GROQ_API_KEY":
                os.environ.setdefault(name.strip(), value.strip().strip("\"'"))


@tool
def get_cpu_config() -> str:
    """Return this computer's CPU model, architecture, core counts, and frequency."""
    frequency = psutil.cpu_freq()
    config = {
        "processor": platform.processor() or "Unknown",
        "architecture": platform.machine(),
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_processors": psutil.cpu_count(logical=True),
    }
    if frequency:
        config["current_frequency_mhz"] = round(frequency.current)
    return json.dumps(config, indent=2)


def build_graph():
    model = ChatGroq(model="openai/gpt-oss-120b", temperature=0).bind_tools([get_cpu_config])

    def ask_model(state: MessagesState):
        return {"messages": [model.invoke(state["messages"])]}

    graph = StateGraph(MessagesState)
    graph.add_node("agent", ask_model)
    graph.add_node("tools", ToolNode([get_cpu_config]))
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")
    return graph.compile()


if __name__ == "__main__":
    load_env_file()
    if not os.environ.get("GROQ_API_KEY"):
        raise SystemExit("GROQ_API_KEY is missing from the environment and .env file.")

    agent = build_graph()
    result = agent.invoke({
        "messages": [
            SystemMessage(content="Use the get_cpu_config tool to report the local CPU configuration accurately."),
            HumanMessage(content="Show my CPU configuration."),
        ]
    })
    print(result["messages"][-1].content)
