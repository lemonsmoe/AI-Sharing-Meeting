# 上下文模板

## Event Template

```md
---
id: EVT-YYYY-MM-DD-HHMM-slug
event_time: 2026-04-17T12:10:00+08:00
recorded_at: 2026-04-17T12:20:00+08:00
agent: 开发2（主agent）
domain: backend
kind: fix
status: done
summary: <一句话概括本次事件>
related_paths:
  - path/to/file
related_commits:
  - abc1234
supersedes: []
---

# Summary

<这次事件是什么>

## What Changed

- <事实 1>
- <事实 2>

## Validation

- <验证方式>

## Follow-ups

- <后续动作>

## References

- <相关域/决策/文档链接>
```

## Domain Template

```md
---
domain: backend
current_status: active
last_event_id: EVT-...
last_event_time: 2026-04-17T12:10:00+08:00
last_recorded_at: 2026-04-17T12:20:00+08:00
owners:
  - 开发2（主agent）
active_branches:
  - main
---

# backend

## Current State

- <当前有效事实>

## Active Work

- <正在进行的工作>

## Blockers

- <阻塞>

## Next Actions

- <下一步>

## Recent Event Links

- [EVT-...](../../02_events/YYYY/MM/EVT-....md)
```

## Decision Template

```md
---
id: DEC-001
status: accepted
domain: docs-process
decided_at: 2026-04-17T12:10:00+08:00
recorded_at: 2026-04-17T12:20:00+08:00
decision_owner: 开发2（主agent）
supersedes: []
---

# DEC-001 标题

## Context

<为什么要做这个决策>

## Decision

- <决策本身>

## Consequences

- <影响>

## Revision Rules

- <以后如何替换/失效>
```

## Handoff Template

```md
---
handoff_id: HOFF-YYYY-MM-DD-slug
created_at: 2026-04-17T12:30:00+08:00
handoff_owner: 开发2（主agent）
related_domains:
  - backend
related_decisions:
  - DEC-001
related_events:
  - EVT-...
---

# 标题

## Current Goal

- <当前目标>

## Stable Facts

- <稳定事实>

## Active Risks

- <风险>

## Read Next

1. <先读哪里>
2. <再读哪里>
```

## Runbook Link Rule

- 项目首次采用该协议时，如果仓库中还没有正式 runbook，应在既有 runbook 区域补建一份。
- `docs/context/` 只存事实和当前态，runbook 负责执行说明。
- runbook 应从 `00_current/index.md`、相关 domain 文档或 handoff 中可达。

## Quick Validation Checklist

- 顶层总览是否没有承载长时间线
- 事件是否按 `event_time` 而不是写入顺序归档
- 域文档是否包含 `last_event_id / last_event_time / last_recorded_at`
- handoff 是否引用域/决策/事件，而不是复制整个历史
- working agent 是否只改了自己涉及的域和事件
- 项目是否已有正式 runbook 入口
