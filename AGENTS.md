# Workspace Guidelines & Agent Rules

## Mandatory Language Policy
- **Strict English Rule**: Regardless of the language used in conversational prompts (e.g., Spanish, French, etc.), **ALL** generated artifacts, code, comments, docstrings, Gherkin feature files (`.feature`), markdown documentation (`.md`), commit messages, and configuration files **MUST BE WRITTEN IN ENGLISH**.

---

## Python Standards
- Follow **PEP 8** style guidelines and conventions.
- Use explicit type hints (`from typing import Optional, List, Dict`, etc.) in classes and function signatures.
- Write meaningful docstrings explaining the purpose and arguments of functions and classes.
- Avoid wildcard imports (`from module import *`).
- Keep code clean, modular, and maintainable.

---

## Playwright & BDD Automation Guidelines

### 1. Page Object Model (POM)
- Page Objects must reside in `pages/` and inherit from `BasePage`.
- Encapsulate locators in `__init__(self, page: Page)`:
  - Prefer user-facing locators: `page.get_by_role()`, `page.get_by_label()`, `page.get_by_text()`, `page.get_by_placeholder()`.
  - For applications with test IDs (like SauceDemo), `page.locator("[data-test='...']")` is standard.
- Page methods must represent user interactions or state queries (e.g., `login(username, password)`, `get_error_message()`).
- **Never place assertions inside Page Object classes**: Page Objects describe UI actions and retrieve state; assertions belong strictly in step definitions.
- For every new Page Object, register it in `pages/page_manager.py` with a typed cache and a property returning its concrete class. Type its constructor (`page: Page`) and public methods so Pylance can navigate from step calls to method definitions.

### 2. Assertions & Resilience
- **Use Web-First Assertions**: Prefer Playwright's `expect` (`from playwright.sync_api import expect`) in step definitions over Python's built-in `assert`.
  ```python
  # Recommended:
  expect(context.page).to_have_url("https://www.saucedemo.com/inventory.html")
  expect(context.pages.login_page.error_message).to_be_visible()
  expect(context.pages.login_page.error_message).to_contain_text("Sorry, this user has been locked out.")
  ```
  `expect` assertions automatically retry until timeouts, eliminating race conditions and flaky tests.
- **No Hardcoded Sleeps**: NEVER use `time.sleep()`. Let Playwright auto-wait for element readiness and states.

### 3. Scenario & Context Isolation
- Tests must be completely independent. Never share state between scenarios.
- Each scenario runs in a dedicated `BrowserContext` created in `features/environment.py`.
- Playwright tracing and failure screenshots must be captured automatically on test failure.

### 4. Gherkin Feature Design
- Feature files reside in `features/` with `.feature` extension.
- Use declarative Gherkin: describe **what** business behavior is tested, not low-level click-by-click mechanics.
- Group related scenarios with descriptive tags (e.g., `@smoke`, `@regression`, `@login`).
- Keep step definitions reusable and organized under `features/steps/`.

### 5. IDE Navigation
- Apply these rules whenever creating or moving a feature, step-definition module, or Page Object; navigation support is part of completing the change, not a one-time setup task.
- Configure `.vscode/settings.json` for Cucumber step discovery:
  - `cucumberautocomplete.steps`: `features/steps/**/*.py`
  - `cucumberautocomplete.syncfeatures`: `features/**/*.feature`
  - `cucumberautocomplete.gherkinDefinitionPart`: `@(given|when|then)\(`
- Keep these globs and the decorator pattern aligned with the actual locations and syntax of all feature and step files.
- Recommend `alexkrechik.cucumberautocomplete` in `.vscode/extensions.json`. This enables navigation from feature steps to their Python step definitions.
- If `.vscode/` is ignored, add narrow `.gitignore` exceptions for the shared `settings.json` and `extensions.json` files.
- Define and reuse a shared `StepContext` protocol in every step-definition module. Annotate the `context` parameter of every step function, and keep the protocol synchronized with all Behave context attributes those functions use. In this project they are `page: Page`, `pages: PageManager`, `config_data: dict[str, Any]`, and `logger: logging.Logger`.
- Whenever adding a step or Page Object, maintain the full chain: feature step → matching decorated step function → typed `PageManager` property → typed Page Object method. Update the shared editor globs if files are placed outside the configured locations.
