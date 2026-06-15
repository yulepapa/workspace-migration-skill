# Sample Audit Output

```md
# Workspace Audit

Total findings: 2

## ai-lab-session

- `~/Documents/Codex/2026-06-15` -> `2_Work/Labs/codex/2026-06` (low)
  - reason: Codex dated session folder

## project-like

- `~/Downloads/example-app` -> `2_Work/Projects/apps` (medium)
  - reason: Project markers found
  - markers: package.json, README.md
```

Treat audit output as a review queue. Do not move path-sensitive items without a manifest, verification, and a rollback path.
