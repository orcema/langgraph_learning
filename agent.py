import os

from langgraph.graph import StateGraph, MessagesState, START
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="openai/gpt-4.1-nano",
    base_url=os.environ.get("LITELLM_BASE_URL", "http://litellm.vlan/v1"),
    api_key=os.environ["LITELLM_API_KEY"],
)


def call_model(state: MessagesState):
    return {"messages": [model.invoke(state["messages"])]}


builder = StateGraph(MessagesState)
builder.add_node("agent", call_model)
builder.add_edge(START, "agent")
graph = builder.compile()


if __name__ == "__main__":
    result = graph.invoke({"messages": [{"role": "user", "content": "Hello, who are you?"}]})
    print(result["messages"][-1].content)
