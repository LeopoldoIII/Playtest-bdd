---
name: bdd-scaffolder
description: >-
  Scaffolds new BDD features, step definitions, and Page Object classes adhering to
  project architecture and English language guidelines. Use this skill when adding
  new tests, creating new page objects, or expanding test coverage.
---

# BDD Scaffolder Skill

This skill outlines the process for implementing new end-to-end test scenarios following the Page Object Model (POM) and Behave step definitions in English.

---

## Architecture Flow

```
1. Feature File (features/<name>.feature)
       ↓
2. Page Object (pages/<name>_page.py)
       ↓
3. Register in PageManager (pages/page_manager.py)
       ↓
4. Step Definitions (features/steps/<name>_steps.py)
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
    def __init__(self, page: Page):
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
Expose the new page through the centralized `PageManager`:

```python
from pages.cart_page import CartPage

class PageManager:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)
        self.inventory_page = InventoryPage(page)
        self.cart_page = CartPage(page)  # Added here
```

---

## Step 4: Implement Step Definitions (`features/steps/<name>_steps.py`)
- Import `given`, `when`, `then` from `behave`.
- Import `expect` from `playwright.sync_api`.
- Access pages via `context.pages.<page_name>`.
- Use `expect` for assertions.

```python
from behave import given, when, then
from playwright.sync_api import expect

@when('the user proceeds to checkout')
def step_proceed_checkout(context):
    context.pages.cart_page.proceed_to_checkout()

@then('the shopping cart badge should display "{count}"')
def step_verify_cart_badge(context, count):
    expect(context.pages.cart_page.cart_badge).to_have_text(count)
```

---

## Validation
Always run the newly created feature to verify step binding and execution:
```bash
./.venv/bin/behave features/<feature_name>.feature
```
