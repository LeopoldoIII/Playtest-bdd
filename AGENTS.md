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
- Register new Page Objects in `pages/page_manager.py` for unified access via `context.pages.<page_name>`.

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
