---
name: bdd-scaffolder
description: >-
  Scaffolds new BDD features, step definitions, and Page Object classes adhering to
  project architecture and English language guidelines. Use this skill when adding
  new tests, creating new page objects, or expanding test coverage.
---

# BDD Scaffolder Skill

This skill outlines the process for implementing new end-to-end test scenarios following the Page Object Model (POM) and Behave step definitions in English.

## Required for Every New BDD File
Treat scaffolding as a connected change, not as creating a single file:
- Every new feature step must have a matching Behave step definition.
- Every new step-definition function must type its `context` with the shared `StepContext`; update that protocol whenever a step uses a new Behave context attribute.
- Every new Page Object must be registered through a typed `PageManager` property and cache.
- Keep the shared VS Code Cucumber globs and decorator pattern valid for all feature and step-definition file locations and syntax.

---

## Navigation Flow

```
Feature File (features/<name>.feature)
       │ Cucumber extension
       ↕
Step Definitions (features/steps/<name>_steps.py)
       │ Pylance (typed context and PageManager)
       ↓
PageManager (pages/page_manager.py)
       │ typed page property
       ↓
Page Object methods (pages/<name>_page.py)
```

---

## Step 1: Create Feature File (`features/<feature_name>.feature`)
- Always write scenarios in **English**.
- Keep steps declarative and business-focused.

```gherkin
@cart
Feature: Shopping Cart Management
  As a shopper
  I want to add products to my cart
  So that I can purchase them during checkout

  Scenario: Add product to cart successfully
    Given the user is logged into the application
    When the user adds "Sauce Labs Backpack" to the cart
    Then the shopping cart badge should display "1"
```

---

## Step 2: Create Page Object (`pages/<name>_page.py`)
- Inherit from `BasePage`.
- Define locators in `__init__`.
- Implement user action methods and query methods.
- Do NOT include assertions in Page Objects.

```python
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage

class CartPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.cart_badge: Locator = page.locator(".shopping_cart_badge")
        self.checkout_button: Locator = page.locator("[data-test='checkout']")

    def proceed_to_checkout(self) -> None:
        self.checkout_button.click()

    def get_cart_count(self) -> str:
        return self.cart_badge.inner_text()
```

---

## Step 3: Register in `pages/page_manager.py`
Expose the new page through the centralized `PageManager`. Annotate its constructor, cached page object, and property with concrete types so Pylance can resolve Page Object methods:

```python
from typing import Optional

from playwright.sync_api import Page

from pages.cart_page import CartPage


class PageManager:
    def __init__(self, page: Page) -> None:
        self.page = page
        self._cart_page: Optional[CartPage] = None

    @property
    def cart_page(self) -> CartPage:
        if self._cart_page is None:
            self._cart_page = CartPage(self.page)
        return self._cart_page
```

---

## Step 4: Implement Step Definitions (`features/steps/<name>_steps.py`)
- Import `given`, `when`, `then` from `behave`.
- Import `expect` from `playwright.sync_api`.
- Access pages via `context.pages.<page_name>`.
- Annotate the `context` parameter in every step definition with the shared `StepContext` protocol. Include each Behave context attribute used by the steps in that protocol; this project uses `page`, `pages`, `config_data`, and `logger`.
- Use `expect` for assertions.

```python
from behave import given, when, then
from playwright.sync_api import expect

from features.steps.step_context import StepContext


@when('the user proceeds to checkout')
def step_proceed_checkout(context: StepContext) -> None:
    context.pages.cart_page.proceed_to_checkout()


@then('the shopping cart badge should display "{count}"')
def step_verify_cart_badge(context: StepContext, count: str) -> None:
    expect(context.pages.cart_page.cart_badge).to_have_text(count)
```

---

The shared protocol can be defined in `features/steps/step_context.py`:

```python
import logging
from typing import Any, Protocol

from playwright.sync_api import Page

from pages.page_manager import PageManager


class StepContext(Protocol):
    page: Page
    pages: PageManager
    config_data: dict[str, Any]
    logger: logging.Logger
```

## VS Code Navigation Setup
Commit these shared workspace settings when bootstrapping the project, and keep them aligned whenever feature or step-definition files are added or moved. Do not add a separate editor configuration for each feature:

`.vscode/settings.json`:
```json
{
  "cucumberautocomplete.steps": [
    "features/steps/**/*.py"
  ],
  "cucumberautocomplete.syncfeatures": "features/**/*.feature",
  "cucumberautocomplete.gherkinDefinitionPart": "@(given|when|then)\\("
}
```

`.vscode/extensions.json`:
```json
{
  "recommendations": [
    "alexkrechik.cucumberautocomplete"
  ]
}
```

If `.vscode/` is ignored, add narrow `.gitignore` exceptions for these two shared files:
```gitignore
!.vscode/
!.vscode/settings.json
!.vscode/extensions.json
```

Install the recommended extension and reload VS Code. Use Cmd+click on macOS (Ctrl+click on other platforms) or F12 to navigate from a feature step to its definition, then from a typed Page Object call to its method. If Page Object navigation does not resolve, verify the `StepContext` and `PageManager` annotations above.

## Validation
Always run the newly created feature to verify step binding and execution:
```bash
./.venv/bin/behave features/<feature_name>.feature
```
