---
name: behave-runner
description: >-
  Runs and debugs Playwright BDD test suites using Behave or BehaveX.
  Use this skill when the user wants to execute tests, run features in parallel,
  filter by tags, run in headed/headless mode, or inspect Playwright traces.
---

# Behave Test Runner Skill

This skill guides test execution and debugging for the Playtest-bdd suite using `behave` and `behavex`.

## Prerequisites
Always ensure you use the virtual environment binaries (`./.venv/bin/behave` or `./.venv/bin/behavex`).

## 1. Running Tests

### Standard Sequential Execution
Run all features:
```bash
./.venv/bin/behave
```

Run a specific feature file:
```bash
./.venv/bin/behave features/login.feature
```

Run scenarios matching specific tags:
```bash
./.venv/bin/behave --tags=@smoke
./.venv/bin/behave --tags="@login and not @slow"
```

Dry-run (validates steps without launching browsers):
```bash
./.venv/bin/behave --dry-run
```

---

## 2. Parallel Execution (via BehaveX)

To execute scenarios or features in parallel across multiple CPU cores:
```bash
# Parallel by scenario (recommended)
./.venv/bin/behavex features/ --parallel-processes 4 --parallel-scheme scenario

# Parallel by feature
./.venv/bin/behavex features/ --parallel-processes 2 --parallel-scheme feature

# Parallel with tag filter
./.venv/bin/behavex features/ -t @login --parallel-processes 2
```
*Note: BehaveX generates consolidated HTML reports in `output/` or `.behavex/`.*

---

## 3. Browser & Execution Configuration

Configuration is driven by `config/settings.json`:
- `"headless"`: `true` (for CI/CD and speed) or `false` (for headed debugging).
- `"browser"`: `"chromium"`, `"firefox"`, or `"webkit"`.

You can also pass Behave defines or override environment variables if configured:
```bash
# Running headed explicitly
HEADLESS=false ./.venv/bin/behave features/login.feature
```

---

## 4. Debugging Failures with Playwright Traces

When a scenario fails, `features/environment.py` saves:
- Screenshot: `reports/screenshots/<scenario_name>.png`
- Trace archive: `reports/traces/<scenario_name>.zip`

To open and inspect the interactive Playwright trace viewer:
```bash
./.venv/bin/playwright show-trace reports/traces/<scenario_name>.zip
```
The trace viewer shows timeline, DOM snapshots, network requests, console logs, and action breakdowns.
