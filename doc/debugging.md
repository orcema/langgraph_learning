# Debugging the LangGraph agent in VS Code

This project has two debug configurations in `.vscode/launch.json`. Pick the one that matches what you need.

## Option 1 — Simple script debug (no web UI)

**Config name:** `Debug LangGraph agent`

Runs `agent.py` directly under the debugger. Good for quickly stepping through the graph logic (e.g. `call_model`) without the LangGraph Studio web UI.

**How to use:**

1. Open the Run and Debug panel (`Cmd+Shift+D`)
2. Select **"Debug LangGraph agent"** from the dropdown
3. Set a breakpoint (e.g. inside `call_model` in `agent.py`)
4. Press F5

This invokes the graph once with the test message defined in `agent.py`'s `if __name__ == "__main__":` block, loads `.env` automatically (via `envFile`), and stops at your breakpoints.

## Option 2 — Full Studio web UI + breakpoints

**Config name:** `Attach to langgraph dev (Studio + breakpoints)`
**Task:** `langgraph dev (wait for debugger)` (`.vscode/tasks.json`)

This runs the real `langgraph dev` server (so you still get the LangGraph Studio web UI, chat panel, and trace view), but with a `debugpy` listener attached so your breakpoints in `agent.py` fire when you send a message from the browser.

**How to use:**

1. Open a terminal in this folder with the venv activated, and run the task:
   - Via Command Palette: **Tasks: Run Task** → `langgraph dev (wait for debugger)`
   - Or directly: `langgraph dev --debug-port 5678 --wait-for-client`
2. Wait for this line in the task output:
   ```
   Debugger listening on port 5678. Waiting for client to attach...
   ```
   The server is paused at this point — it will not start serving requests or open the browser until a debugger attaches.
3. Open the Run and Debug panel, select **"Attach to langgraph dev (Studio + breakpoints)"**, and press F5.
4. VS Code attaches to the waiting process, the server resumes, and LangGraph Studio opens in your browser.
5. Set breakpoints in `agent.py` (e.g. in `call_model`). They will hit when you send a chat message from the Studio web UI.

### Known gotcha: don't wire the task as a `preLaunchTask`

An earlier version of `launch.json` set `"preLaunchTask": "langgraph dev (wait for debugger)"` on the attach config, intending a single F5 to both start the task and attach. **This causes attach to hang/fail if the task is already running** (e.g. you started it manually first): VS Code's background-task detection only "completes" once per matched output line, and if that line already appeared before you triggered the debug session, the attach step never proceeds.

The fix applied in this project: the attach config has **no** `preLaunchTask`. Always run the task first (step 1 above), confirm it's waiting (step 2), *then* start the attach debug config (step 3). This two-step flow is reliable; a single-button flow is not, given this interaction.

### Verifying the listener is alive

If attach seems to hang, confirm the debugpy socket is actually listening before troubleshooting further:

```bash
lsof -nP -iTCP:5678 -sTCP:LISTEN
```

You should see the `langgraph dev` python process bound to `127.0.0.1:5678`. If nothing is listed, the task isn't running (or already consumed a prior attach) — stop and restart it via step 1.

### Orphaned debugpy process / "Address already in use"

If a debug session gets stopped abnormally (e.g. closing the terminal panel instead of using VS Code's Stop button), the `debugpy` adapter process can be left running and holding port 5678. The next time you start the task, `langgraph dev` fails with:

```
RuntimeError: Can't listen for client connections: [Errno 48] Address already in use
```

This is handled automatically now: the task runs a `free port 5678` step first (`.vscode/tasks.json`), which kills anything already listening on 5678 before starting `langgraph dev`. You shouldn't need to do this manually anymore. If you ever want to check/clear it by hand:

```bash
lsof -ti tcp:5678 | xargs kill -9
```

## Files involved

| File | Purpose |
|---|---|
| `.vscode/launch.json` | The two debug configurations described above |
| `.vscode/tasks.json` | `free port 5678` (kills anything on 5678 first) → `langgraph dev (wait for debugger)` (starts `langgraph dev --debug-port 5678 --wait-for-client`) |
| `.vscode/settings.json` | Points VS Code at the project's `venv` interpreter |
| `agent.py` | The graph definition; `if __name__ == "__main__":` block is the entry point for Option 1 |
| `.env` | `LITELLM_BASE_URL` / `LITELLM_API_KEY` — loaded automatically by the debug configs |
