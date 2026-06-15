# Workspace Taxonomy

Use this reference to classify local folders and files before any migration.

## Priority Rule: Project Context First

Project context overrides file type.

If a file or folder was created for, used by, or needed to understand a specific project, event, client workstream, Tableau build, app, automation, or AI-assisted implementation, keep it inside that project capsule.

Use shared library folders only when the material is reusable outside any one project.

Examples:
- A Viz Games recording belongs in the Viz Games project capsule, not global `Assets`, if it is needed to understand or continue Viz Games work.
- A Tableau workbook export belongs in its Tableau project capsule when it is part of that project's iteration history.
- A dataset belongs in `3_Library/Data` only when it is standalone or reused across projects. If it is project-specific, keep it in the project `data` folder.
- A final PDF belongs in `4_Archive/Outputs` only when it is a shareable or archived output copy. The project source and context copy stay in the project capsule.

Suggested project capsule shape:

```text
2_Work/Projects/{domain}/{project-name}/
  README.md
  docs/
  data/
  assets/
  recordings/
  workbooks/
  outputs/
  references/
  scripts/
  experiments/
  backups/
  archive/
```

Suggested subfolders are optional. Create them only when the project actually has matching content or the tool/framework expects that folder. Do not split a project into global buckets just to satisfy the folder names above.

## Canonical Workspace Roots

### `0_Inbox`

Temporary intake for unsorted files. Use when the item's final category is unknown or when it came from Desktop, Downloads, screenshots, messages, browser exports, or one-off AI output.

Suggested subfolders:

```text
0_Inbox/
  downloads/
  desktop-drop/
  screenshots/
  received-files/
  to-sort/
```

Rules:
- Keep this small and temporary.
- Do not run long-term projects from here.
- Sweep weekly or whenever it grows enough to become noisy.

### `1_Now`

Return checkpoint index. Use it to recover current context quickly, not to store source files or mirror active projects.

Suggested subfolders:

```text
1_Now/
  README.md
```

Rules:
- Prefer one `README.md` with canonical paths over many symlinks.
- Keep symlinks minimal. Use them only for a few frequently reopened active items.
- Do not store unique files here unless they are temporary.
- Do not use `1_Now` as a full project list, diary, or live task tracker.
- Include only workstreams where a future resume would otherwise lose context.
- Keep source material in `2_Work`, `3_Library`, or `4_Archive`.

Include a `1_Now/README.md` entry when most of these are true:

- there is a live next action
- context recovery would likely take more than 10 minutes without a checkpoint
- context spans multiple paths, reports, sessions, bridges, or tools
- a recent move, merge, rename proposal, bridge, or canonical switch could cause confusion
- opening the wrong path could break execution, data links, tool state, or project continuity
- the work is likely to resume within 14 days
- verification, use-cycle confirmation, or bridge retirement is still pending

Exclude or prune an entry when most of these are true:

- the work is complete or archived
- there is no next action
- the canonical path plus project README/report is enough to resume
- it is unlikely to be touched within 14 days
- it is a simple reference, final output, app state, system folder, or whole-project inventory entry
- a recently changed path has passed use-cycle verification and the bridge state is stable

Do not prune by age alone. If a path or verification risk remains after 14 days, keep a shortened `Paused` or `Recently Changed Paths` entry.

### `2_Work`

Active work. It has two durable sub-roots: `Projects` and `Labs`.

```text
2_Work/
  Projects/
  Labs/
```

#### `2_Work/Projects`

Canonical home for long-lived working projects. Use for Git repos, apps, MCP servers, automations, data apps, maintained Tableau projects, mobile apps, and personal tools.

Suggested subfolders:

```text
2_Work/Projects/
  apps/
  data-apps/
  tableau/
  mcp/
  automation/
  mobile/
  content-tools/
  client-work/
  personal/
```

Rules:
- A folder belongs here if it has source code, a durable project identity, or future continuation value.
- Creation tool does not matter. Codex/Claude/Antigravity-created projects move here when they become durable.
- Keep repo roots intact.
- Do not keep duplicate canonical copies.
- Project-owned subfolders stay with the project by default.
- Use copy-verify-switch for project migration. A copied repo is only a pilot until the canonical path has been switched and verified.

#### `2_Work/Labs`

Experiments, one-off AI sessions, prototypes, research spikes, generated trials, and date-based work folders.

Suggested subfolders:

```text
2_Work/Labs/
  codex/
    YYYY-MM/
  claude/
    YYYY-MM/
  antigravity/
    YYYY-MM/
  cursor/
    YYYY-MM/
  gemini/
    YYYY-MM/
  playgrounds/
```

Rules:
- Use tool names here because session provenance matters.
- Keep date folders by month.
- Promote durable work to `2_Work/Projects`; leave a symlink or note from the old lab path during transition.
- Codex App may continue creating new sessions under `~/Documents/Codex`. Treat those folders as intake/compatibility paths and sweep inactive sessions into `2_Work/Labs/codex/YYYY-MM`.
- Preserve old Codex session paths as hidden symlinks when Codex, process-manager history, or shell history may still refer to them.
- Do not move the currently active Codex session folder.

### `3_Library`

Shared reusable material. It contains `Knowledge`, `Data`, `Assets`, and `Tools`.

```text
3_Library/
  Knowledge/
  Data/
  Assets/
  Tools/
```

#### `3_Library/Knowledge`

Reference material, study notes, courses, documentation, manuals, reading material, and Obsidian-style knowledge vaults.

Rules:
- Store knowledge by topic, not by source app.
- Keep generated summaries here only if they are reusable knowledge.
- Keep project-specific docs inside the project unless they are general reference.
- Evidence logs and historical transcripts usually stay with the project or migration report that produced them.

#### `3_Library/Data`

Standalone or shared datasets and processing material.

Rules:
- Keep raw data immutable where practical.
- Put processing scripts in the related project or `3_Library/Tools/scripts`.
- Link project data folders to canonical data when needed.
- Do not extract nested project data into `3_Library/Data` just because it contains CSV, JSON, logs, or exports.

#### `3_Library/Assets`

Reusable media and design/source assets.

Rules:
- Use for reusable assets, not final deliverables.
- Keep app-generated cache out of here.
- Move project-specific assets into the project when only one project uses them.
- Do not pull `public`, `assets`, screenshots, or generated images out of an app/game project unless the asset is intentionally shared across projects.

#### `3_Library/Tools`

Reusable tooling, local utilities, templates, MCP servers, CLI tools, browser extensions, and setup helpers.

Rules:
- Use this for tools that support other projects.
- If a tool is itself a maintained product/project, `2_Work/Projects` may be better.
- Keep install archives in `4_Archive/backups` or `4_Archive/deprecated` unless actively used.

### `4_Archive`

Inactive, old, completed, deprecated, preserved, or externally shareable material.

Suggested subfolders:

```text
4_Archive/
  Outputs/
  deprecated/
  backups/
  old-desktop/
  old-downloads/
  installers/
```

Rules:
- Archive only after verifying no active tool depends on the old path.
- Prefer date-stamped archive folders for bulk migrations.
- Do not archive app-owned state folders as part of normal workspace organization.
- Use `4_Archive/deprecated/` for old real folders that were replaced by hidden compatibility symlinks.
- Use `4_Archive/backups/` for config backups, migration manifests, and pre-edit safety copies.
- Use `4_Archive/Outputs/` for independent reports, exported deliverables, and migration reports.

## Compatibility Bridge Map

Old Workspace numeric names may still exist as hidden symlinks:

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

Rules:
- These are compatibility paths, not canonical storage paths.
- Do not create new durable content using old numeric paths.
- Do not delete a bridge until the relevant tools have completed at least one normal use cycle from the new path.

## Path-Sensitive Detection Signals

Before classifying by file type, decide whether the item is path-sensitive. Path-sensitive means a move, rename, archive, or deletion could break execution, references, history, or external identity.

Use signals instead of hardcoded product lists:

- project identity: repository metadata, manifests, build files, README/title files, notebooks, service definitions, workbook/project bundles
- references: paths inside code, configs, scripts, shortcuts, notebooks, workbooks, launch settings, shell history, symlinks, or agent/MCP/tool configs
- runtime: active cwd, live process, local server, watcher, task runner, virtual environment, generated dependency tree, local database, active editor/session state
- external identity: deployed URL, Git remote, package name, app/service name, published dashboard, browser extension ID, sync identity, user-facing project name
- ownership: app-owned/global state, hidden tool folders, IDE/editor settings, local credentials, auth/session material, application support directories
- bundled formats: workbooks, packaged project files, databases, media libraries, archives, design/document bundles, or any format likely to contain embedded links
- containment: inside an already-detected project capsule, tool state folder, generated dependency folder, or app-owned directory

Examples include Git repos, Tableau workbooks, MCP servers, Streamlit apps, browser extensions, Obsidian vaults, Python/Node environments, `.env` files, editor folders, and app support folders. The examples can expand over time; the detection signals are the rule.

## Classification Decision Tree

1. Is it app/tool-owned state, protected runtime material, or cache under an app-owned location?
   - Yes: do not move as part of workspace migration.
2. Is it inside an existing project capsule or path-sensitive workspace?
   - Yes: keep it with the owner unless the project-specific migration plan says otherwise.
3. Is it a durable project, app, repo, workbook/project bundle, automation, tool, or service root?
   - Yes: `2_Work/Projects` or `3_Library/Tools` depending on whether it is a product/project or a support tool.
4. Is it a bundled or internally linked format, local database, media/design library, workbook, extract, packaged project, or repository owned by a desktop app?
   - Yes: defer to a domain-specific batch with link/reference verification.
5. Is it an AI/tool date session, prototype, or one-off generated workspace?
   - Yes: `2_Work/Labs/{tool}/YYYY-MM`.
6. Is it general learning/reference material?
   - Yes: `3_Library/Knowledge`.
7. Is it raw/cleaned/exported data?
   - Yes: `3_Library/Data`.
8. Is it reusable media/design material?
   - Yes: `3_Library/Assets`.
9. Is it a final export, report, or deliverable copy?
   - Yes: project `outputs/` if project-owned, otherwise `4_Archive/Outputs`.
10. Is it old but worth preserving?
   - Yes: `4_Archive`.
11. Is classification uncertain?
   - Yes: `0_Inbox/to-sort`.

## Automation And Rename Decision Tree

1. Is the item app-owned state, protected runtime material, a live process cwd, or the current active session?
   - Yes: do not move or rename. Document it as deferred or do-not-touch.
2. Is the item a loose file with no project owner and an obvious category?
   - Yes: it can be moved automatically to the correct Workspace bucket.
3. Is the loose file name generic but the context is clear from metadata, parent folder, or contents?
   - Yes: it can be auto-renamed using the naming rules, then moved.
4. Is the item part of a project, path-sensitive workspace, app, automation, bundled project, or event workstream?
   - Yes: keep or restore it inside one project capsule. Preserve the existing name unless there is an approved rename batch.
5. Is the proposed change a path-sensitive rename, identity change, link-bearing format change, runtime-state change, or config/reference-bound path change?
   - Yes: produce a rename proposal requiring approval. Include old path, new path, references found, bridge plan, verification, and rollback.
6. Is the project identity ambiguous because several folders overlap?
   - Yes: use strongest identity evidence in this order: external/deployed identity, remote/sync identity, package/app/service config, README/title, folder contents, then local folder nickname.
7. Would moving or renaming separate related context?
   - Yes: keep the context together in the project capsule, even if file types differ.

## Naming Rules

- Top-level folders: use exactly `0_Inbox`, `1_Now`, `2_Work`, `3_Library`, `4_Archive`.
- Second-level folders should normally use semantic names without numeric prefixes, such as `Projects`, `Labs`, `Knowledge`, `Data`, `Assets`, `Tools`, `codex`, `tableau`, `obsidian`, `recordings`, `browser-extensions`, or `local-sdks`.
- Add numbering only when order is operationally meaningful, such as `01_raw`, `02_cleaned`, `03_exports`, or a documented project pipeline.
- Do not keep empty deep placeholder folders merely to mirror suggested examples. Suggested subfolders are options, not required folders.
- Keep empty folders only when they are structural roots, active workflow indexes, compatibility bridges, or app/project internals that tools may expect.
- Do not rename existing project/tool paths just to add numbering. Path stability is more important than visual consistency after tools have remembered a path.
- New public/code project folders: prefer lowercase `kebab-case` unless the repo, package, deployed service, or public URL already uses another stable identity.
- Existing Korean names are acceptable, and often preferable, for human-facing study/reference folders, Tableau/event projects, personal workstreams, and project names whose meaning is clearer in Korean.
- Date folders: use `YYYY-MM` for monthly AI/tool buckets and `YYYY-MM-DD-topic` for dated loose documents or session summaries.
- Loose document names should combine date or source with a human topic, for example `2026-06-15-workspace-sweep.md`, `viz-games-feedback-notes.md`, or `sales-export-cleaned.csv`.
- Avoid canonical names such as `final`, `final_final`, `new`, `test`, `data`, `image`, `수정본`, `복사본`, and `untitled` unless they are inside temporary, generated, or app-owned folders.
- Do not rename while relocating path-sensitive roots. First move with existing names; rename only in a later pass after stale-reference search and use-cycle verification.

## Agent, IDE, And App Tool Rules

- Agents, IDEs, desktop apps, local servers, notebooks, and app builders may remember old absolute paths. Codex, Claude Code, Antigravity, Cursor, Gemini, VS Code, Tableau, Obsidian, and browser extension tooling are examples.
- Preserve old paths with hidden symlinks during the transition when a project was recently active or when tool metadata/history may still reference it.
- Before replacing an old path with a symlink, check whether the path is the current working directory or is used by a live process. Defer active paths.
- Stale history or process-manager references alone do not require keeping a real folder in place if a hidden symlink preserves the old path.
- Tool default creation paths are not assumed to follow the Workspace taxonomy. Sweep known intake roots periodically instead of assuming new sessions appear in Workspace.
- Keep project-local tool metadata with the project unless there is a specific cleanup plan. Examples include hidden agent, IDE, editor, and workflow folders.
- Do not move global state, credential, auth/session, or app support folders as ordinary workspace cleanup. Examples include hidden home-directory tool folders and `~/Library/Application Support/...`.

## Project Verification Checklist

Before declaring a migrated project successful:

- `git status` works if the folder is a repo.
- Stale absolute paths were searched.
- Package manager install/build/test commands were run when applicable.
- Path-bearing configs, scripts, launch settings, environment files, app manifests, and tool metadata were checked for old paths.
- The relevant agent, IDE, app, local server, or desktop tool can open the new root.
- Old path symlink exists when old tool state may still reference it.

## Generated And Reproducible Artifact Handling

Prefer regeneration over migration for reproducible runtime artifacts such as dependency folders, build outputs, caches, test outputs, virtual environments, and compiled bytecode.

Examples:

- `node_modules`
- `.next`
- `dist`
- `build`
- `.turbo`
- `test-results`
- `.venv`
- `venv`
- `__pycache__`

Do not delete generated folders unless the user has asked for cleanup or the migration plan explicitly lists them. Preserve them when regeneration is impossible or the folder is actually project data, not a reproducible artifact.

## Completion Language

Use precise completion labels:

- `batch complete`: the named manifest was applied and verified.
- `pilot copied`: the new location exists, but the old path is still canonical.
- `canonical switched`: tools and humans should use the new path.
- `old path preserved`: symlink or compatibility bridge exists.
- `full migration complete`: all planned batches are applied, verified, and remaining inventory is intentionally empty or deferred.

Never report a pilot copy or narrow batch as the full local-folder reclassification.
