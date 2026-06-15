# Workspace Migration Skill

A Codex skill for auditing and safely migrating local folders into a stable `~/Workspace` structure.

The skill is designed for people who want a practical local information architecture for projects, AI coding sessions, reusable library material, and archives without breaking path-sensitive tools.

## Structure

The default workspace shape is:

```text
~/Workspace/
  0_Inbox/
  1_Now/
  2_Work/
    Projects/
    Labs/
  3_Library/
    Knowledge/
    Data/
    Assets/
    Tools/
  4_Archive/
    Outputs/
    deprecated/
    backups/
```

## What This Skill Emphasizes

- Project context first: project-owned data, assets, outputs, docs, and recordings stay in the project capsule.
- `1_Now` as a small return checkpoint, not canonical storage.
- Copy-verify-switch migration for path-sensitive projects.
- Hidden symlink bridges when tools may remember old paths.
- Read-only audit before any filesystem change.

## Files

- `SKILL.md`: main skill instructions
- `references/taxonomy.md`: folder taxonomy and classification rules
- `scripts/workspace_audit.py`: read-only audit helper
- `agents/openai.yaml`: Codex skill metadata
- `examples/`: sample outputs and customization notes
- `assets/social-preview.png`: GitHub social preview image

## Install

Copy or symlink this folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R workspace-migration ~/.codex/skills/workspace-migration
```

Then invoke it from Codex as `workspace-migration`.

## Audit

Run the read-only audit:

```bash
python3 scripts/workspace_audit.py --format md
```

Scan additional roots explicitly:

```bash
python3 scripts/workspace_audit.py --root ~/Desktop --root ~/Downloads --root ~/some-folder --format md
```

## Privacy

This public template avoids personal absolute paths and does not include migration logs, session state, private reports, credentials, or local runtime folders.
