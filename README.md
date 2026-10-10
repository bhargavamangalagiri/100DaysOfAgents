# 100 Days of AI Agents

Learning Python and building AI agents through small, runnable experiments.

## First milestone: tool calling

The `tool_calling` example looks up fictional support tickets. It demonstrates:

1. Describing a Python tool to a model through OpenRouter.
2. Reading the model's structured tool request.
3. Validating arguments and executing the function locally.
4. Sending the tool result back for a final answer.

## Setup

Use Python 3 (developed with Python 3.14).

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Set `OPENROUTER_API_KEY` in your terminal environment before running the model example. Do not put your actual key in source code or commit it. The script reads the environment directly; it does not automatically load `.env` files.

## Run

Local checks, without API calls:

```bash
python tool_calling/tool_call.py
```

Model and tool round trip:

```bash
python tool_calling/model_call.py
```

The example requests `nvidia/nemotron-3-super-120b-a12b:free`. Availability and free-tier limits can change.

This is a learning example with one round of tool execution, not a production agent. Its dispatcher validates the inputs for one tool and assumes the outer request has the expected fields.

## Daily Git workflow

```bash
git status
git diff
git add <specific-files>
git diff --staged
git commit -m "Describe what changed"
git push
```

A commit saves a local snapshot. A push sends commits to the configured remote repository. Review the staged changes before committing.
