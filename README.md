# LangGraph Learning

A minimal LangGraph agent, wired up to a local LiteLLM gateway, for learning/testing LangGraph.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install langgraph langchain-openai "langgraph-cli[inmem]"
```

Copy `.env` and set `LITELLM_BASE_URL` / `LITELLM_API_KEY` for your local LiteLLM gateway.

## Run

```bash
source venv/bin/activate
langgraph dev
```

Opens LangGraph Studio in the browser for interacting with the agent.

## Debugging

See [doc/debugging.md](doc/debugging.md) for how to debug the agent in VS Code, including running LangGraph Studio with breakpoints attached.
