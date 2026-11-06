# Runbook Template

Use this template when a project needs a formal runbook for the context-management workflow.

## Required Sections

- Purpose
- Minimal handoff contract
- When to use `$context-management`
- Multi-agent Git/worktree isolation rule
- Project context layout
- Reading order
- Responsibility-to-domain mapping
- Role split: working agent / main agent / optional curator agent
- Minimum update steps for event, domain, decision, and handoff
- Time and conflict rules
- Runbook maintenance rules
- Project-specific domain mapping

## Placement Rule

- Prefer the repository's existing runbook area, such as `docs/runbooks/`
- If no runbook area exists, place it in the project's accepted stable-docs area
- Link the runbook from the current-state entrypoint so new agents can discover it quickly

## Minimal Handoff Contract Guidance

The runbook should make it possible for a user to hand work to another agent with only:

1. the new agent's responsibility
2. a short explanation of what the project is for
3. an instruction to use `$context-management`

The runbook should then define:

- what to read first
- what to read next
- what to update
- what not to update
- when to drill into recent events

## Multi-Agent Git Isolation Guidance

If a project expects multiple parallel implementation tasks or multiple agents producing commits, the runbook should explicitly require:

1. one active implementation task per worktree
2. one task branch per worktree
3. use of [$git-multi-task-collaboration](C:/Users/22796/.codex/skills/git-multi-task-collaboration/SKILL.md) for branch/worktree setup and recovery workflow
4. one integration agent to merge or cherry-pick accepted work into the accepted baseline
