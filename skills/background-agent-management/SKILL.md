---
name: background-agent-management
description: >
  Governs safe handling of background subagent (run_in_background=true) results.
  TRIGGER whenever: launching background agents, waiting for agent completions, or dispatching
  multiple parallel agents. Prevents result loss from temp file expiry, enforces partial delivery
  as each agent completes (no silent batching), enforces timeout detection with auto-switch to
  direct execution, and mandates TodoWrite visibility per agent. Use proactively — load this skill
  BEFORE dispatching any background agent, not after results go missing.
---

# Background Agent Result Management

This skill was forged from a real failure: three parallel background agents were dispatched,
one timed out silently, another's temp file expired, the user waited in silence and had to ask twice.
These four rules prevent that from happening again.

---

## The Four Rules

### Rule 1 — Persist Immediately on Completion

The moment a background agent completes, **write its results to a permanent file before anything else**.
Temp files under `AppData/Local/Temp/` or `/tmp/` expire — sometimes within minutes.
They are not a reliable storage medium.

Write to:
- A vault note (Obsidian work) — e.g., `Gaoyan Projects/ProjectName/agent-output.md`
- A project file — any path that is not in a temp directory

**Pattern:**
```
Agent notification arrives
  → TaskOutput block=true (collect result)
  → Write to permanent file
  → Notify user with summary
```

**Anti-pattern (causes data loss):**
```
Agent notification arrives
  → Plan to summarize later          ← DON'T
  → Temp file quietly expires        ← Result gone
  → User asks, you can't recover it  ← Trust broken
```

---

### Rule 2 — Deliver Partially, Never Batch in Silence

When multiple background agents are running in parallel, **deliver each result immediately as it arrives**.
Do not wait for all agents to finish before saying anything.

**Correct:**
```
Agent A completes  → "[Agent A 完成] 调研发现：..."  (immediate output)
Agent B completes  → "[Agent B 完成] 调研发现：..."  (immediate output)
Agent C completes  → "[Agent C 完成] 调研发现：..."  (immediate output)
→ Then synthesize all three
```

**Wrong:**
```
Agent A completes  → (silence, waiting for B and C)
Agent B completes  → (silence)
Agent C never completes → (user waits, asks "还没好吗？")   ← this happened
```

The user should never wait in silence for more than one minute after an agent completes.

---

### Rule 3 — Timeout Detection and Auto-Switch

| Time since last agent notification | Action |
|------------------------------------|--------|
| 2 minutes | Proactively tell the user: "Agent X is still running, estimated another N minutes" |
| 4 minutes | Announce: "Switching to direct execution" — do the task yourself using WebSearch/WebFetch/Read |

**On auto-switch:**
1. Announce clearly: "Agent [name] did not complete in time — executing directly"
2. Execute the task inline using available tools
3. Do NOT spin up another background agent for the same task

The user's time matters. Four minutes of silence is unacceptable.

---

### Rule 4 — TodoWrite Per Agent

Every `run_in_background=true` launch gets its own TodoWrite entry.
Update status in real time: `pending` → `in_progress` → `completed`.

```json
{
  "content": "Research CDI management team [Agent A]",
  "status": "in_progress",
  "activeForm": "Researching CDI management team"
}
```

Mark `completed` only after the result has been **written to a permanent file** (Rule 1).
This gives the user live visibility into what is and isn't done.

---

## Pre-Flight Checklist

Before using `run_in_background=true`, confirm:

- [ ] Where will I write the permanent results file? (path must exist or be creatable)
- [ ] Is this genuinely a long-running task (>3 min)? If not, use foreground instead
- [ ] Does each agent have a TodoWrite entry?
- [ ] Am I prepared to switch to direct execution if an agent times out?

---

## Foreground-First Default

**`run_in_background=false` is the default.** Use background only when:

1. Expected runtime genuinely exceeds 3 minutes, AND
2. You have independent work to do in parallel, AND
3. You have a permanent path ready to receive results

If uncertain, use foreground. Results cannot be lost, the user sees progress, and there is no timeout risk.

---

## When Background Goes Wrong

If you discover a background agent's result is gone (temp file expired, task ID not found,
output file empty):

1. **Announce immediately** — do not pretend nothing happened
2. **Switch to direct execution** — use WebSearch/WebFetch/Read to do it yourself
3. **Do not re-launch** another background agent for the same task
4. **Deliver the result** via direct execution and move on

Example announcement:
> "Agent [X] 的结果文件已过期，无法恢复。我直接重新执行这部分调研。"

---

## Environment Note (This Vault)

On this Windows machine, temp paths expire quickly:
- ❌ `C:\Users\杨顺\AppData\Local\Temp\claude\` — expires
- ✓ `C:\Users\杨顺\Documents\Obsidian Vault\` — permanent vault, use this

When writing agent results to the vault, use the appropriate project folder:
- Research outputs → `Gaoyan Projects/<ProjectName>/`
- Knowledge base → `高岩知识库/`
- Temp analysis → `Gaoyan Projects/<ProjectName>/temp-analysis/`

---

## Summary Card

| Rule | Trigger | Action |
|------|---------|--------|
| 1 — Persist immediately | Agent completes | Write to vault file before anything else |
| 2 — Partial delivery | Any agent completes | Output that result NOW, don't wait for others |
| 3 — Timeout | 2 min silence → check; 4 min → switch | Announce + execute directly |
| 4 — TodoWrite | Agent launched | One todo per agent, update on completion |
