# ProsperAI Agent Framework v0.3

Runnable foundation for ProsperAI's reusable AI-agentic platform.

This repository is deliberately **framework-first** rather than feature-first. The sample Collections flow proves the architecture, but the framework is designed so future CFO, Cash Flow, Compliance, Payables, Payroll, Operations, Risk and Growth agents can be added without redesigning the core.

## What works now

- Thin orchestrator as the single AI-work coordinator.
- Modular input guardrail pipeline.
- Baseline prompt-injection blocking and PII masking extension points.
- Deterministic-first planning.
- Dependency-aware task executor with bounded parallelism.
- Reusable agent registry.
- Provider-agnostic `ModelGateway` with timeout/error normalization.
- Mock LLM provider so the project runs with **no API key**.
- Multiple logical MCP servers grouped by domain.
- Per-agent tool allow-lists.
- Execution-time tool authorization.
- Tool timeout/error normalization.
- Tool/model output guardrail hooks.
- Deterministic business-rule enforcement outside the LLM.
- Approval lifecycle for protected actions.
- Fresh-state revalidation before approved execution.
- Idempotency protection against duplicate protected actions.
- Tenant and correlation context propagation.
- Safe structured telemetry abstraction.
- 14 deterministic unit/integration-style tests.

## Core execution flow

```text
AgentRequest
   ↓
Input Guardrails
   ↓
Planner (deterministic first)
   ↓
TaskExecutor
   ↓
Specialist Agent
   ├── allowed MCP/domain tools
   └── ModelGateway when reasoning is needed
   ↓
ActionProposal
   ↓
WorkflowEngine
   ↓
RuleEngine          ← deterministic hard rules
   ↓
ApprovalPolicy
   ↓
PENDING_APPROVAL
   ↓
Human APPROVE / MODIFY / REJECT
   ↓
Fresh business-state read
   ↓
Rule revalidation
   ↓
Protected tool execution
   ↓
COMPLETED + idempotent result
```

## Important security boundary

Agents **do not directly mutate protected business state**. They analyse and propose actions. The `WorkflowEngine` is the hard execution boundary and business rules are deterministic code/policy, not an LLM judgement.

The regex prompt-injection and PII controls are intentionally basic reference implementations. They prove the extension points; they are **not production-grade security controls**.

## Sync vs async

This implementation follows the current ProsperAI design decision:

- normal interactive service calls are synchronous/awaited;
- Python `async/await` is used for I/O and parallel independent tasks;
- queues/event buses are **not** inserted between every component;
- messaging can be added later for long-running jobs, background processing, retries/decoupling, proactive events or higher-volume workloads.

## Run locally

Requires Python 3.11+. The project has **no runtime third-party dependency** for the mock foundation.

### Fastest no-install path

From the repository root:

```bash
python run_demo.py
python run_tests.py
```

This works directly from `src/` and does not require pip or internet access.

### Optional editable install

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install (requires setuptools to be available in the environment):

```bash
pip install -e .
```

Then run:

```bash
python -m prosperai_agent_framework.demo
```

If package installation is unavailable, use `python run_demo.py` instead.

The demo performs:

1. request validation and PII masking;
2. Collections routing;
3. authoritative invoice read;
4. model-backed recommendation using the mock provider;
5. deterministic rule validation;
6. `PENDING_APPROVAL`;
7. human approval;
8. fresh invoice re-read;
9. rule revalidation;
10. reminder action;
11. repeated execution proving idempotency.

## Tests

```bash
python run_tests.py
```

Expected result: **14 tests pass**.

## Environment settings

Optional framework settings:

```text
PROSPERAI_MAX_PARALLEL_TASKS=4
PROSPERAI_MODEL_TIMEOUT_SECONDS=30
PROSPERAI_TOOL_TIMEOUT_SECONDS=15
PROSPERAI_MAX_REQUEST_CHARS=20000
```

No model API key is needed for the current runnable version because it uses `MockLLMProvider`.

## Current project structure

```text
src/prosperai_agent_framework/
├── agents.py          # BaseAgent, AgentRegistry, CollectionsAgent
├── bootstrap.py       # dependency wiring / runtime builder
├── demo.py            # end-to-end executable example
├── executor.py        # dependency-aware bounded concurrency
├── guardrails.py      # input + tool/model payload guardrail hooks
├── llm.py             # LLMProvider + ModelGateway + mock provider
├── mcp.py             # MCP adapter abstraction, multi-server registry, tools
├── models.py          # shared contracts, statuses and normalized errors
├── orchestrator.py    # thin coordinator
├── planner.py         # deterministic-first planner interface
├── settings.py        # environment-driven non-secret settings
├── telemetry.py       # safe structured telemetry abstraction
└── workflow.py        # rules, approval, idempotency and execution boundary
```

See `ARCHITECTURE.md` for deeper design notes and `CHANGELOG.md` for changes from v0.1.


## Presentation UI (v0.3)

v0.3 adds a Streamlit presentation UI wired to the **same framework runtime**.

### Install UI dependency

From the project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[ui]"
```

### Start the UI

```powershell
.\.venv\Scripts\python.exe run_ui.py
```

or double-click / run:

```text
run_ui.bat
```

Streamlit will print a local URL, normally:

```text
http://localhost:8501
```

The UI demonstrates:

- orchestrator entry point,
- critical-data, prompt-injection and PII guardrails,
- sanitized request before delegation,
- deterministic planning,
- agent selection,
- MCP server grouping,
- per-agent tool allow-lists,
- model gateway/provider abstraction,
- hard deterministic business rules,
- human approval,
- fresh-state revalidation,
- idempotency,
- unauthorized-tool denial,
- dependency-aware parallel executor capability,
- structured telemetry.

See `PRESENTATION_DEMO_GUIDE.md` for a short board-demo script.
