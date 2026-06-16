---
name: workspace-migration
description: Organize, audit, and safely migrate a user's local folders into a stable ~/Workspace hierarchy. Use when the user wants to restructure Desktop, Downloads, Documents, Codex/Claude/Antigravity/Cursor/Gemini work folders, AI coding sessions, project folders, data, assets, outputs, archives, or when creating a non-destructive migration plan with symlink and verification safeguards.
---

# Workspace Migration

## Operating Mode

Treat this as a local information-architecture and migration skill. The default outcome is a stable, usable `~/Workspace` with project context preserved and old tool paths kept working.

Do not move, rename, delete, or archive files in the first pass. First produce an inventory or dry-run plan. Execute moves only when the user explicitly asks to apply the plan or has already approved the current migration branch.

Read `references/taxonomy.md` whenever the task needs folder meanings, subfolder choices, naming rules, or migration decisions.

## Canonical Root

The current canonical physical structure is:

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

Compatibility bridges may exist at the old top-level names:

```text
00_Inbox -> 0_Inbox
10_Active -> 1_Now
20_Projects -> 2_Work/Projects
30_Labs -> 2_Work/Labs
40_Knowledge -> 3_Library/Knowledge
50_Data -> 3_Library/Data
60_Assets -> 3_Library/Assets
70_Outputs -> 4_Archive/Outputs
80_Tools -> 3_Library/Tools
90_Archive -> 4_Archive
```

Treat those old numeric paths as hidden compatibility bridges only. Do not create new canonical content there.

## Structure Rules

- Project context overrides file type. If a file or folder was created for, used by, or needed to understand a project, keep it inside that project capsule instead of scattering it into global `Data`, `Assets`, `Outputs`, or `Knowledge`.
- Durable projects live under `~/Workspace/2_Work/Projects/{domain}/{project-name}`.
- AI sessions, experiments, generated trials, and research spikes live under `~/Workspace/2_Work/Labs/{tool}/YYYY-MM/`.
- Shared knowledge, data, reusable assets, and support tools live under `~/Workspace/3_Library/`.
- Project-specific outputs stay in the project capsule. Independent final/published exports and migration reports live under `~/Workspace/4_Archive/Outputs/`.
- `1_Now` is a return checkpoint index, not canonical storage. Prefer a single `README.md` with canonical paths. Keep symlinks minimal and only for a few frequently reopened active items.
- Use numeric prefixes only for the five top-level Workspace roots. Ordinary second-level folders should use semantic names without numeric prefixes.
- Use second-level numbering only for ordered pipelines where order is part of the workflow, such as `01_raw`, `02_cleaned`, `03_exports`.
- Keep stable project and tool paths more important than cosmetic renaming. Do not rename a migrated project just to match a naming preference until the path has survived a normal use cycle.
- `_Start` was retired as an active entry layer after the five-root physical migration. If found, treat it as historical/deprecated unless a new plan explicitly restores it.
- Do not precreate or preserve empty deep placeholder folders just because a taxonomy example mentions them. Keep only the five-root structure, its required structural children, and folders that contain real content, links, active workflow meaning, or app/tool-required structure.
- Remove empty placeholders only with `rmdir` after confirming they are outside project internals, app-owned folders, Tableau Repository internals, and compatibility bridge paths.

## Desktop And Finder-Visible Items Protocol

Do not assume every icon visible on the macOS Desktop is a file under `~/Desktop`.

When the user asks why Desktop items remain, classify the visible item into one of these surfaces before planning moves:

- real Desktop file or folder under `~/Desktop`
- hidden compatibility symlink bridge under `~/Desktop`
- Finder-visible mounted volume under `/Volumes`, such as an opened `.dmg` installer
- macOS metadata, such as `.DS_Store` or `.localized`

For Desktop checks, inspect both the Desktop directory and mounted volumes:

```bash
find ~/Desktop -maxdepth 1 -print -exec ls -ldO {} \;
ls -laO /Volumes
mount
hdiutil info
```

Mounted installer volumes are not Workspace migration candidates. Do not move `/Volumes/*` into Workspace. If a volume is an app installer, first verify the app exists in `/Applications`, then treat the volume as an eject candidate and treat the source `.dmg` file, if still present in Downloads or Inbox, as a separate loose-file cleanup candidate.

Safe installer-volume handling:

```bash
ls -ldO /Applications/AppName.app
hdiutil detach "/Volumes/AppName"
```

If the app is not installed, if the mounted volume is writable user storage, or if the volume identity is unclear, do not detach automatically. Report it as a high-risk or manual-review item.

## 1_Now Checkpoint Protocol

Use `~/Workspace/1_Now/README.md` as a small return checkpoint, not as a live task tracker, diary, or project list.

Purpose:

- help the user or a future agent resume work without losing context
- point to canonical project locations under `2_Work`, `3_Library`, or `4_Archive`
- record only the minimum state needed to avoid re-discovery
- keep unique source files out of `1_Now`

Default structure:

```text
~/Workspace/1_Now/
  README.md
```

Use symlinks sparingly. Prefer README entries over symlinks unless an item is actively reopened often and a symlink clearly reduces friction. Do not turn `1_Now` into a mirror of active projects.

Update `1_Now/README.md` during workspace-migration work when a project or workstream is created, moved, merged, renamed, paused, resumed, canonical-switched, symlink-bridged, or left with follow-up verification that may matter within the next 14 days.

Include an item only when most of these are true:

- it has a live next action
- losing context would likely cost more than 10 minutes to recover
- context spans multiple paths, reports, sessions, bridges, or tools
- a recent move, merge, rename proposal, bridge, or canonical switch could cause confusion
- opening the wrong path could break execution, data links, tool state, or project continuity
- it is likely to be resumed within 14 days
- verification, use-cycle confirmation, or bridge retirement is still pending

Exclude or remove an item when most of these are true:

- it is complete or archived
- it has no next action
- the canonical path plus project README/report is enough to resume
- it is unlikely to be touched within 14 days
- it is a simple reference, final output, app state, system folder, or whole-project inventory entry
- a recently changed path has passed use-cycle verification and the bridge state is stable

Do not remove an entry only because it is older than 14 days. If risk or next action remains, keep a shortened `Paused` or `Recently Changed Paths` entry.

Use this template when creating or refreshing the file:

```md
# Now

Last updated: YYYY-MM-DD

Update rule:
- Update after starting, pausing, resuming, moving, merging, renaming, canonical-switching, or completing a project.
- Keep only checkpoints likely to matter in the next 14 days or still carrying path/verification risk.
- Keep source files in their canonical locations.

## Active Checkpoints

### Project or Workstream
- Canonical:
- Status:
- Next:
- Risk:
- Notes:

## Paused

### Project or Workstream
- Canonical:
- Resume when:
- Notes:

## Recently Changed Paths

### Project or Workstream
- Canonical:
- Old path:
- Bridge:
- Verify:
```

Automation limitation: the agent can update `1_Now/README.md` only for work it observes or performs. Work done manually or in other apps is not automatically visible; if needed, the user can explicitly ask to update `1_Now`.

## Context-Aware Automation Levels

Use the highest safe automation level that matches the evidence and user authorization.

- Level 0: read-only audit. Inventory, classify, and report. No filesystem changes.
- Level 1: dry-run plan. Propose moves, renames, symlinks, verification, and rollback points. No filesystem changes.
- Level 2: low-risk auto-move. Move loose, project-independent files from Desktop, Downloads, Documents, or Inbox into the correct Workspace bucket when the destination is unambiguous and no active process/tool state depends on the old path.
- Level 3: project capsule consolidation. Move or merge project-owned files back into one capsule only after building a manifest, preserving old paths with hidden symlinks when tools may remember them, and verifying the target.
- Level 4: canonical rename or identity change for any path-sensitive object. Require explicit user approval for the rename batch when an item has internal references, external references, runtime state, deployment identity, tool ownership, bundled project formats, or active-process risk.

Default behavior: classify automatically, apply only Level 2 and already-approved Level 3 work, and turn Level 4 into a concrete approval list.

## Path-Sensitive Object Detection

Do not rely on a fixed list of tools or file extensions. Before moving, renaming, archiving, or deleting, classify whether the item is path-sensitive.

Treat an item as path-sensitive when any signal suggests that changing its path could break execution, links, history, or external identity:

- project identity signal: repository metadata, package/app manifests, build files, README/title files, workbook/project bundles, notebooks, or service definitions
- reference signal: absolute or relative paths inside code, configs, scripts, shortcuts, notebooks, workbooks, metadata files, launch settings, shell history, MCP/tool configs, or symlinks
- runtime signal: current working directory, live process, local server, watcher, task runner, virtual environment, generated dependency tree, database, cache that cannot be safely regenerated, or active editor/session state
- external identity signal: deployed URL, Git remote, package name, app/service name, published dashboard, browser extension ID, cloud/local sync identity, or user-facing project name
- ownership signal: app-owned/global state, hidden tool folders, IDE/editor settings, local credentials, auth/session material, or application support directories
- bundled-format signal: files or folders whose internals may contain links or embedded references, such as workbooks, packaged project files, databases, media libraries, archives, and design/document bundles
- containment signal: the item is inside an already-detected project capsule, tool state folder, generated dependency folder, or app-owned directory

Examples include Git repos, package projects, Tableau workbooks, MCP servers, Streamlit apps, browser extensions, Obsidian vaults, Python/Node environments, `.env` files, editor folders, and app support folders. These are examples, not the rule.

Path-sensitive default actions:

- do not auto-rename
- do not split by file type
- keep context together in the owning capsule or app/tool location
- use copy-verify-switch for migrations
- search stale references before switching
- leave a hidden symlink bridge when old paths may be remembered
- propose Level 4 changes as an approval list with verification and rollback

## Naming And Rename Policy

The skill may infer better names, but it must not blindly rename everything.

- Decide context owner before naming. A name must reflect the project, workstream, source, date, or artifact role, not only the file extension.
- Preserve existing project and tool folder names during first relocation. Path stability is more important than cosmetic consistency while tools may remember old absolute paths.
- Auto-rename only low-risk loose files when the current name is generic, duplicated, or unusable and the new name can be inferred from nearby context, metadata, or file contents.
- Do not auto-rename path-sensitive objects. Propose those renames in a Level 4 approval list with evidence, stale-reference search, bridge plan, verification, and rollback.
- New project folders should normally use stable semantic names under `2_Work/Projects/{domain}/{project-name}`. Prefer lowercase `kebab-case` for new public/code projects; keep Korean names for human-facing study, Tableau, event, or personal work where that is the clearer identity.
- If a deployed app, Git remote, package name, or public URL already establishes identity, that identity wins over a local nickname. Example: prefer `image_convert` over a duplicate local working nickname when the deployed app identity is `imageconvert` and the code matches.
- For dated loose documents, prefer `YYYY-MM-DD-topic.ext`. For monthly AI sessions, prefer `YYYY-MM/<original-folder-name>` under the relevant lab tool.
- Avoid names such as `final`, `final_final`, `new`, `test`, `data`, `image`, `수정본`, or `복사본` as canonical names unless they are inside a temporary or generated folder.
- Before any rename that could affect tools, search for stale references, verify no live process uses the old path, then leave a hidden symlink bridge for directories when practical.

## Workflow

1. State the target result: stable workspace structure, minimal breakage, reversible migration.
2. Run a read-only audit before planning:

```bash
python3 scripts/workspace_audit.py --format md
```

3. Classify candidates using `references/taxonomy.md`.
4. Before applying file-type classification, assign a context owner:
   - project owner, if the item belongs to a project, event, client workstream, Tableau build, app, automation, or implementation
   - tool/session owner, if it is only an AI session or experiment
   - shared/global, if it is reusable outside any one project
   - unknown, if it needs manual review
5. Separate plans into batches by risk and ownership, not only by tool name:
   - project-context restoration for already-scattered project-owned files
   - low-risk loose intake files from Desktop, Downloads, Documents, Inbox, and similar user drop zones
   - path-sensitive durable projects and code/app workspaces
   - AI/tool lab sessions and generated work areas
   - bundled or linked project formats that need domain-specific verification
   - app/tool-owned state and protected runtime material
   - archives, backups, and final independent outputs
6. For each move, define:
   - current path
   - proposed path
   - category and reason
   - risk level
   - verification command or manual check
   - whether to leave a hidden symlink bridge
   - automation level, from Level 0 to Level 4
   - rename decision: keep name, safe auto-rename, or approval-required rename
7. Keep original names during first relocation. Rename only after the new location has worked for at least one use cycle.
8. Prefer copy-verify-switch for important projects. Use direct move only for low-risk loose files, same-volume project-capsule restoration where old paths are immediately bridged, or when the user explicitly requests it.
9. After moving any path-sensitive item, search for stale absolute paths and old compatibility roots. Expand the pattern when the manifest found additional old roots:

```bash
rg "~|Documents/Codex|Desktop|Downloads|Workspace/20_Projects|Workspace/30_Labs|Workspace/40_Knowledge|Workspace/50_Data|Workspace/60_Assets|Workspace/70_Outputs|Workspace/80_Tools|Workspace/90_Archive" .
```

10. Prefer regenerating reproducible runtime artifacts after relocation instead of treating them as canonical content. Examples: virtual environments, dependency folders, build outputs, caches, test results, and compiled bytecode. Preserve only when regeneration is impossible or the project-specific plan requires it.
11. Leave temporary hidden symlinks from old paths to new paths for path-sensitive items that may be remembered by agents, IDEs, editors, local servers, workbooks, scripts, browser extensions, MCP configs, shell history, or app metadata.
12. For old paths that must remain only for compatibility, prefer hidden symlinks over deletion:

```bash
ln -s "$new_path" "$old_path"
chflags -h hidden "$old_path"
```

13. Before switching old paths used by Codex or local servers, check live process risk:

```bash
ps -axo pid=,stat=,etime=,command= | rg "old/path|project-name|server-command"
```

If a process is active, defer the switch. If only stale process-manager/history references remain, keep the old path as a hidden symlink.

14. After every applied batch, rerun the audit and document:
   - remaining audit candidates
   - Finder-visible top-level entries in Desktop, Downloads, Documents, home, and Workspace
   - Finder-visible mounted volumes under `/Volumes` and whether they are installer eject candidates or real storage
   - broken symlink checks for relevant old and new paths
15. After every applied batch, decide whether `1_Now/README.md` needs a checkpoint update:
   - add or update entries for active, paused, recently changed, or verification-risk workstreams
   - prune or shorten entries whose next action and path risk are gone
   - do not add full project inventories or completed items with no next action
16. Never call a batch "complete" as if the whole local migration is complete. Report the completion level explicitly:
   - batch complete
   - project pilot copied
   - canonical switch complete
   - old path preserved
   - full workspace migration complete

## Hard Rules

- Do not reorganize app-owned or global tool state folders. Examples include hidden home-directory tool folders and `~/Library/Application Support/...`, but the rule is ownership-based, not name-based.
- Do not move the active working directory of the current conversation. If the current cwd is inside a migration candidate, defer that candidate and document it.
- Do not move `/Volumes/*` into Workspace. Mounted volumes are device or disk-image surfaces, not canonical files. Eject installer volumes only after app installation is verified; leave writable or unclear volumes for manual review.
- Do not assume Codex App creates new sessions in `~/Workspace`. New Codex sessions may continue to appear under `~/Documents/Codex`; handle them with the Codex Session Sweep Protocol.
- Do not move `~/Documents/Codex/.omx` while the old Codex root may still be in use.
- Do not move bundled or internally linked project formats in a generic loose-file batch. Use a domain-specific batch with link/reference verification. Tableau workbooks, packaged workbooks, extracts, databases, design bundles, document bundles, and media libraries are examples.
- Do not mix "tool used" with "project identity": real projects go under `2_Work/Projects` even if created inside an AI tool, IDE, notebook, app builder, or temporary session folder.
- Keep tool-specific names mainly under `2_Work/Labs`.
- Do not delete old locations until the new location has been verified and any needed symlink transition period is complete.
- Do not over-normalize project-owned files into global buckets. A project-specific recording, screenshot, dataset, workbook, export, script, note, or reference belongs inside the project capsule unless it is intentionally shared across projects.
- Do not treat hidden compatibility symlinks as failed migration. They are intentional bridges when old absolute paths may still be remembered by tools.
- Do not treat nested project folders as standalone migration candidates just because they look like data, assets, docs, outputs, settings, or generated artifacts. Keep project-owned content, source, evidence, settings, tool folders, and generated folders with their project unless the project migration plan says otherwise.
- Do not perform Level 4 renames without an explicit approval list, even when the proposed name is clearly cleaner.
- Do not remove old-path bridges until the new canonical path has passed at least one normal use cycle or the user explicitly asks to retire the bridge.

## State And Document Contract

Use one report directory per migration date:

```text
~/Workspace/4_Archive/Outputs/reports/workspace-migration/YYYY-MM-DD/
```

Keep these documents current:

```text
migration-master-plan-vN.md          # human entry point and full-scope plan
remaining-inventory-after-stepN.md   # current state after the last applied batch
next-batch-plan-vN.md                # next executable dry-run plan
migration-execution-report.md        # what was actually applied, not the whole ambition
```

Execution artifacts should live beside them:

```text
*-manifest.tsv
evidence/
quality-gate.json
```

Rules:
- The master plan is the canonical human-facing plan.
- Inventory documents are snapshots, not promises.
- Next-batch plans are dry-run plans until the user explicitly asks to apply them.
- Execution reports must distinguish "applied", "not applied yet", "verification", and "remaining risks".
- If a previous report overstates completion or uses old canonical paths, correct the report before continuing.

## Batch Strategy

Prefer this order unless the user gives a different priority:

1. Project-context restoration for already-scattered project-owned files.
2. Loose Desktop/Downloads files that have no project owner.
3. Durable path-sensitive project candidates with copy-verify-switch.
4. Bundled or internally linked formats with domain-specific link/reference verification.
5. AI/tool lab work areas, promoting durable projects to `2_Work/Projects`.
6. Knowledge, study, and personal documents only when they are project-independent.
7. Shared data and media bulk groups only when they are project-independent.
8. Transition cleanup for symlinks, duplicate pilots, deprecated entry layers, and temporary inbox items.

Important project states:

```text
candidate -> copied -> verified -> use-cycle-ok -> canonical-switched -> old-path-symlinked -> archive/delete-decision
```

Do not collapse these states. A copied project is not migrated until the canonical switch is verified.

## Recurring Sweep

For periodic maintenance, run the audit script, then produce a sweep report with these sections:

```text
New inbox items
Project candidates
Project-context restoration candidates
Lab/session candidates
Data candidates
Asset/output candidates
Archive candidates
Do-not-touch app/tool state
High-risk items needing manual review
Suggested next batch
Safe auto-move candidates
Rename proposals requiring approval
Bridge retirement candidates
Finder-visible mounted volumes
1_Now checkpoint updates
```

The sweep report should recommend moves but avoid applying them unless the user asks. Low-risk Level 2 moves may be applied only when the user has already asked the agent to continue maintenance autonomously. Level 4 rename proposals remain approval-required.

## Project Capsule Protocol

Use this when a workstream has related files scattered across `3_Library`, `2_Work/Labs`, `4_Archive/Outputs`, old numeric Workspace paths, or old Desktop/Downloads/Documents locations.

1. Create or identify one canonical project capsule under `~/Workspace/2_Work/Projects/{domain}/{project-name}`.
2. Build a context-owner manifest with:
   - source path
   - current bucket
   - context owner
   - confidence
   - proposed capsule path
   - move type
   - risk
   - verification
   - old-path bridge decision
3. Prefer `rsync -a` copy into the capsule first, then verify with `rsync -ain`.
4. Switch old paths only after verification:
   - directories: replace with hidden symlink when tools may remember the old path
   - files: keep old path as a symlink or leave a documented duplicate until use-cycle verification
5. Add `README.md` or `INDEX.md` at the capsule root that explains the internal layout and current canonical files.
6. For domain capsules, keep internally linked files, data, assets, scripts, outputs, references, recordings, and verification evidence together when they were part of the same project. Do not split them into global buckets unless they are intentionally shared.
7. Do not call the context restoration complete until old paths still resolve and the capsule contains enough context to continue the project without searching global folders.

## Codex Session Sweep Protocol

Use this when new folders appear under `~/Documents/Codex`.

1. Treat `~/Documents/Codex` as an intake/compatibility surface, not the canonical destination.
2. Classify dated Codex session folders into:
   - active current cwd: defer
   - live process cwd: defer
   - stale process-manager/history only: safe to switch with hidden symlink
   - inactive session: safe to sync and switch
3. Canonical destination:

```text
~/Workspace/2_Work/Labs/codex/YYYY-MM/<original-folder-name>
```

4. Use `rsync -a` to sync source to the Workspace target, then require a clean source-to-target dry run before switching:

```bash
rsync -a "$old_path/" "$new_path/"
rsync -ain "$old_path/" "$new_path/"
```

5. Move the old real folder to `~/Workspace/4_Archive/deprecated/` before creating the hidden symlink.
6. Update active path-bearing config references only after backing up the config and validating its format. For Codex sessions, `~/.codex/config.toml` is a known example and requires TOML parsing verification.
7. Leave the old path as a hidden symlink until at least one normal use cycle confirms Codex can work from the Workspace path.
8. Do not move `~/Documents/Codex/.omx` while a current or recent Codex root may still depend on it.
