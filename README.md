# Playwright BDD Framework (Python) 🚀

Welcome to the Playwright BDD automation framework! This project is designed specifically to help users transition from **Selenium** to **Playwright** using **Behave** (Python's native BDD framework).

It incorporates enterprise-level best practices like the Page Object Model (POM), Custom Logging, Environment Variables management, and Allure Reporting.

---

## 🛠️ Setup Instructions

---

### 1. Pre-requisites
Ensure you have Python 3.9+ installed on your system.

### 2. Install Dependencies
We use a virtual environment to keep dependencies clean.

```bash
# Create a virtual environment (if not already created)
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Install Playwright Browsers
Playwright requires you to download the browser binaries (Chromium, Firefox, WebKit).

```bash
playwright install
```

### 4. Environment Variables
Copy the sample environment file to create your local `.env`:
```bash
cp .env.example .env
```
This file stores your base URL and test credentials securely without hardcoding them in `.feature` files.

---

## 🏃‍♂️ Running the Tests

We use `behave` to run the feature files.

### Basic Execution
```bash
# Run all tests
behave

# Run a specific feature file
behave features/login.feature
```

### 🏷️ Filtering with Tags
You can filter which tests to run using tags (`@smoke`, `@regression`) defined in your feature files.

```bash
# Run only smoke tests
behave --tags=@smoke

# Run regression tests, but exclude smoke tests
behave --tags=@regression --tags=~@smoke
```

---

## 📊 Allure Reporting & Tracing

---

This framework is configured to automatically generate high-quality HTML reports using Allure, and Playwright Traces for deep debugging.

### Generating the Report
To run tests and generate allure results:
```bash
behave -f allure_behave.formatter:AllureFormatter -o allure-results
```

To view the generated report in your browser:
```bash
# Install allure commandline if you haven't (requires Java/Brew/NPM)
# e.g., brew install allure
allure serve allure-results
```
*Note: If a test fails, a screenshot will automatically be attached to the Allure report!*

### Playwright Traces ⏱️
If a test fails, a `trace_*.zip` file will be saved in the `logs/` directory. Traces are like a time-machine for your tests (showing DOM snapshots, console logs, and network requests).
To view a trace:
```bash
playwright show-trace logs/trace_Failed_Login_Attempts.zip
```

---

## 🆚 Selenium vs Playwright Cheat Sheet

---

Transitioning from Selenium? Here is how common commands translate to Playwright.

| Action | Selenium (Python) | Playwright (Python) | Notes |
|--------|-------------------|---------------------|-------|
| **Navigate to URL** | `driver.get("https://...")` | `page.goto("https://...")` | Playwright auto-waits for the `load` event. |
| **Find Element** | `driver.find_element(By.ID, 'foo')` | `page.locator('#foo')` | `locator` is lazy; it doesn't search the DOM until an action is performed. |
| **Robust Locators**| `driver.find_element(By.XPATH, "//*[text()='Login']")`| `page.get_by_role("button", name="Login")` | Playwright encourages user-facing locators (`get_by_role`, `get_by_text`). |
| **Click Element** | `element.click()` | `page.locator('#foo').click()` | Playwright **auto-waits** for the element to be visible, stable, and clickable! |
| **Type Text** | `element.send_keys("hello")` | `page.locator('#foo').fill("hello")` | `fill()` clears the input first. Use `type()` for emulating keystrokes. |
| **Wait for Visible**| `WebDriverWait(driver, 10).until(EC.visibility_of_element_located(...))` | `page.locator('#foo').wait_for(state='visible')` | Usually unnecessary in Playwright due to auto-waiting on actions. |
| **Wait for Hidden** | `WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(...))` | `page.locator('#foo').wait_for(state='hidden')` | Very simple syntax in Playwright. |
| **Iframes** | `driver.switch_to.frame("frame_name")`<br>`element.click()`<br>`driver.switch_to.default_content()` | `page.frame_locator('#frame_name').locator('#foo').click()` | No need to "switch" contexts! Just chain the locators. |
| **Exceptions** | `NoSuchElementException`, `TimeoutException` | `playwright.core.TimeoutError` | Handled using `try...except playwright.core.TimeoutError`. |

### 🧠 Key Concept: Web-First Assertions (`expect`)
In Selenium, checking if an element's text changes requires complex `WebDriverWait` logic. In Playwright, you use `expect`, which automatically retries the assertion until it passes or times out:

```python
from playwright.sync_api import expect

# Automatically waits up to 5 seconds for the text to appear
expect(page.locator(".error")).to_have_text("Invalid Login")
```

---

## 🏗️ Architecture Overview

- **`features/`**: Contains the BDD Gherkin files (`.feature`) and the `environment.py` (hooks like `before_all`, `after_scenario`).
- **`features/steps/`**: Contains the Python code that glues the Gherkin steps to the Page Object Model.
- **`pages/`**: Contains the Page Object classes (`base_page.py`, `login_page.py`, etc.).
- **`utils/`**: Contains utility classes (`logger.py` for execution logs, `playwright_utils.py` for advanced Playwright methods).
- **`config/`**: Contains JSON configuration (e.g., setting the browser to chromium/firefox/webkit or headless mode).

---

## 🚀 Must-Know Playwright Concepts & Best Practices

---

To master Playwright, you should be familiar with these core concepts and automation best practices:

### 🧠 Core Concepts
1. **Browser Launch:** The initial step where the browser engine (Chromium, WebKit, Firefox) is instantiated (either headless or headed).
2. **Browser Context:** Isolated sessions (like Incognito) created from the browser. They allow parallel execution, clean test isolation, and multi-user simulation without launching multiple heavy browsers.
3. **Page Instance:** Represents a single browser tab within a context. You use it to navigate (`page.goto()`) and extract page-level data (`page.title()`, `page.url()`).
4. **Locators (Core Strength):** The mechanism to find elements. Playwright locators are lazy-evaluated and come with strictness checks and auto-waiting built-in.
5. **Auto-Waiting (No `sleep`):** Playwright automatically waits for elements to be Visible, Enabled, and Stable (not animating) before performing actions.
6. **Web-First Assertions:** Smart assertions like `expect(locator).to_be_visible()` that automatically retry until they pass or timeout, eliminating flakiness.
7. **Test Runner:** Playwright comes with its own powerful test runner offering parallel execution and built-in reporting (in Python, this role is filled by `pytest-playwright` or `behave`).
8. **Fixtures:** Reusable setup/teardown logic injected into tests, making tests cleaner, faster, and CI/CD ready.
9. **Network Interception:** The ability to intercept, mock, or modify API requests (`page.route()`) to improve stability and test the frontend independently.
10. **Parallel Execution:** Running tests concurrently across multiple workers for faster builds and scalable automation.
11. **Test Configuration:** Global settings (like timeouts, retries, viewports, and browser types) usually defined in a central config file or environment variables.
12. **Page Object Model (POM):** A design pattern that represents web pages as classes, keeping test logic separate from locators.
13. **Shadow DOM Piercing:** Playwright's default locators (`css`, `text`) automatically pierce open Shadow DOMs, removing the need for complex JavaScript injections to interact with web components.
14. **Frames and Iframes (`frame_locator`):** Playwright allows you to seamlessly target elements inside iframes by chaining locators (e.g., `page.frame_locator().locator()`), without needing to manually switch contexts.
15. **Trace Viewer & Debugging:** A powerful built-in tool that captures DOM snapshots, console logs, and network requests at every test step, essentially providing a "time machine" for debugging failed CI runs.
16. **API Testing (`page.request`):** Playwright isn't just for UI testing. It has a built-in API request context that allows you to send HTTP requests to seed data, validate backend endpoints, or set up test preconditions blazingly fast.
17. **Codegen (Test Generator):** The `playwright codegen` CLI command records your manual browser interactions and generates automation scripts automatically, serving as a huge time-saver for writing boilerplate code.

### ⭐ Best Practices
- **Use user-centric locators:** Prefer `get_by_role`, `get_by_label`, or `get_by_text` over CSS or XPath.
- **Avoid XPath:** Use it only when absolutely required (it's slower and harder to read).
- **Write independent tests:** Tests should be idempotent and runnable in any order without relying on shared state.
- **Rely on web assertions & auto-wait:** Never use `time.sleep()`. Let Playwright's `expect` and auto-waiting do the heavy lifting.
- **Capture screenshots/traces on failure:** Always configure your runner to capture artifacts on failure for easy debugging.
- **Keep data separate:** Use test data files (JSON/CSV) instead of hardcoding values in scripts.
- **Run headless in CI/CD:** Always execute tests in headless mode in the pipeline to save resources and speed up execution.

## 🎓 Playwright Manual & Interview Guide

---

If you are transitioning from Selenium or preparing for a technical interview, this section covers the core concepts, architectural differences, and frequently asked questions.

### 🏛️ Architecture: Selenium vs Playwright



**Selenium WebDriver Architecture:**
- **How it works:** Selenium uses the WebDriver protocol (traditionally based on the HTTP/JSON Wire Protocol, now standardized by W3C).
- **The flow:** Your code (Python) -> sends an HTTP request -> to the local driver (`chromedriver`, `geckodriver`) -> which communicates with the actual browser.
- **Main drawback:** Relying on individual HTTP requests for commands introduces higher latency. To synchronize states, it relies on polling via `WebDriverWait`, which can lead to flaky tests.

**Playwright Architecture:**
- **How it works:** Playwright skips HTTP and communicates **directly** with the browser engine using native debugging protocols (like the **Chrome DevTools Protocol - CDP** for Chromium).
- **The flow:** Your code establishes a **single, bidirectional WebSocket connection** with the browser.
- **Main advantage:** Through the WebSocket, Playwright receives events from the browser *in real-time* (e.g., "DOM loaded", "network is idle", "element X is now visible"). This makes its **Auto-waiting** possible, resulting in incredibly fast and stable tests without writing explicit waits.

### ✅ Advantages of Playwright
1. **Auto-waiting:** Before clicking a button, Playwright automatically checks that it is attached to the DOM, visible, stable (no ongoing animations), enabled, and not obscured by other elements.
2. **Web-first Assertions:** Functions like `expect(locator).to_be_visible()` automatically retry the assertion in a loop until it passes or the timeout is reached, eliminating false negatives caused by UI micro-delays.
3. **Lightning-fast Browser Contexts:** Playwright uses isolated "Contexts" that act as independent incognito sessions. Creating a context takes milliseconds, allowing you to run multiple isolated tests or test multi-user flows (e.g., Admin vs. Client) within a single open browser.
4. **Network Interception:** Native support for blocking requests (e.g., heavy images, ads) or mocking API responses using `page.route()`, ideal for testing the frontend independently of the backend.
5. **Top-tier Debugging Tools:** Includes the *Trace Viewer* (a "time machine" to inspect the DOM, console, and network at the exact moment a test fails) and the Inspector/CodeGen.
6. **Dependency Management:** It downloads and manages its own browser binaries (`playwright install`). No more `chromedriver` version incompatibility issues.

### ❌ Disadvantages / Limitations of Playwright
1. **Real Mobile Devices:** Playwright emulates mobile devices very well (resolution, user-agent, touch), but it **does not** run on actual native mobile devices (Appium or native tools are still required for that).
2. **Legacy Browser Support:** It does not support older browsers like Internet Explorer 11. It is 100% focused on modern browsers (Chromium, Firefox, WebKit).
3. **Historical Community:** Although it is growing rapidly, Selenium has been around for much longer. You will find more historical documentation and old forum answers for Selenium.

---

### 🗣️ Common Interview Questions

---

**1. What is "Auto-waiting" and how does it work?**
*Answer:* It's Playwright's ability to ensure an element is ready before performing an action. Before an event like `click()`, Playwright performs a sequence of checks: it ensures the element is attached to the DOM, visible, its bounding box is stable (not animating), and it can receive pointer events. If any check fails, it waits asynchronously until the timeout is reached.

**2. How does Playwright handle iframes and multiple tabs compared to Selenium?**
*Answer:* In Selenium, you must manually switch context (`driver.switch_to.frame()` or `.window()`) and switch back to the default content. In Playwright, **you don't need to switch focus**. For iframes, you chain locators: `page.frame_locator("#my_frame").locator("#my_button").click()`. For tabs, you manage independent `page` instances generated from the `context`, acting on them in parallel.

**3. What is the difference between `fill()` and `type()`?**
*Answer:* `fill()` is the preferred action: it clears any existing text in the input and dispatches the necessary events to insert the new text almost instantly. `type()` simulates pressing key by key (`keydown`, `keyup`, `keypress`); it is slower but useful if you need to trigger keystroke-sensitive autocomplete scripts.

**4. What is a Browser Context and why is it important?**
*Answer:* A Context is an isolated browsing session (with its own cookies, cache, and local storage). It's crucial because instead of opening and closing a heavy browser for each test (as you would in Selenium to ensure a clean state), in Playwright you launch a browser once and create ultra-lightweight contexts for each test, drastically reducing execution times.

**5. What would you do if Playwright cannot interact with an element because it is covered by another (e.g., a floating modal or cookie banner)?**
*Answer:* You could use the click method with the force parameter: `element.click(force=True)`. This bypasses the check that ensures the element receives pointer events and injects the click directly into the center of the element in the DOM. This is useful for complex scenarios, although the best practice would be to close the cookie modal first.

**6. How do you handle elements which are inside a Shadow DOM?**
*Answer:* One of Playwright's greatest strengths is that its standard locators (`css`, `text`, etc.) pierce open Shadow DOMs by default. Unlike Selenium, where you have to inject JavaScript (`shadowRoot`) to access elements inside a web component, in Playwright you just locate the element as if it were in the regular DOM: `page.locator(".my-shadow-element")`.

**7. How do you handle multiple windows or tabs?**
*Answer:* Playwright manages multiple pages/tabs asynchronously through the Browser Context. Instead of iterating through window handles and switching contexts like in Selenium, you wait for the `page` event when an action triggers a new tab:
```python
with context.expect_page() as new_page_info:
    page.get_by_text("Open new tab").click()
new_page = new_page_info.value
new_page.wait_for_load_state()
print(new_page.title())
```

**8. What is the Page Object Model (POM) and how does it differ from Page Factory?**
*Answer:* The Page Object Model is a design pattern that creates an object repository for web UI elements, making code reusable and maintainable. In Playwright, you create classes representing pages, passing the `Page` object in the constructor. *Page Factory* is a Selenium-specific concept (using `@FindBy` annotations in Java) to lazily initialize elements. Playwright does not need or use Page Factory because its `locator()` objects are strictly lazy-evaluated by design—they don't resolve against the DOM until an action (like `click()`) is performed.

**9. How do you execute only a specific suite of tests (e.g., Regression) in Behave?**
*Answer:* You use tags. In your `.feature` files, you tag scenarios or features with `@regression`. During execution, you pass the `--tags` argument via CLI: `behave --tags=@regression`. You can also use logical operators, for example, `behave --tags=@regression --tags=~@smoke` to run regression tests excluding smoke tests.

**10. How do you pass tabular data to a step in Behave (without using Scenario Outline)?**
*Answer:* You use Data Tables. Underneath the Gherkin step, you write a Markdown-like table. In your Python step definition, this table is accessible via the `context.table` object. You can iterate over it using a simple loop:
```python
# Gherkin:
# Given the user adds the following items:
#   | item       | quantity |
#   | laptop     | 1        |

# Python:
@given("the user adds the following items:")
def step_impl(context):
    for row in context.table:
        print(f"Adding {row['quantity']} of {row['item']}")
```

**11. What is the root cause of "flakiness" in UI automation, and how does Playwright fix it?**
*Answer:* Flakiness (tests that randomly pass or fail without code changes) is primarily caused by synchronization issues (the script executing faster than the browser rendering elements or network resolving). In Selenium, you manually mitigate this with explicit waits (`WebDriverWait`), which is error-prone. Playwright solves this natively via **Auto-waiting**: before acting on an element, Playwright automatically ensures the element is in the DOM, visible, stops moving, and is ready to receive events.

**12. How do you integrate Playwright tests into a CI/CD pipeline (e.g., Jenkins, GitHub Actions)?**
*Answer:* Playwright is highly CI/CD friendly because it operates in a headless mode by default. The typical process involves:
1. Setting up a Python environment in the pipeline.
2. Installing dependencies (`pip install -r requirements.txt`).
3. Installing the Playwright browsers using `playwright install --with-deps` (the `--with-deps` flag ensures OS-level dependencies are also installed on the runner).
4. Executing the test command (e.g., `behave`).
5. Archiving the generated Allure results and Playwright Traces as build artifacts.

**13. How would you test for broken links on a page efficiently using Playwright?**
*Answer:* Instead of clicking every link and waiting for a page load (which is very slow), you can extract all `href` attributes and validate them concurrently. Playwright includes an integrated API request context (`page.request`) that you can use to ping the URLs without leaving the browser session. By combining Python's `asyncio` (or `concurrent.futures`) with Playwright's API context, you can send HEAD/GET requests to all links in parallel and assert that the status codes are 200.

---

## 🤖 AI in QA Interview Questions (2026 Edition)

---

As AI becomes integral to software development, interviewers increasingly ask about your experience with AI tools and testing AI applications.

**1. How are you using AI in your daily testing work?**
*Answer:* I use AI to generate test cases, create automation code snippets (like complex locators and regex), write SQL queries, generate API payloads, and summarize requirements. It helps me save time, but I always review and validate the output before integrating it into the framework.

**2. Which AI tools have you used?**
*Answer:* I have used tools like ChatGPT, Claude, and GitHub Copilot. They assist with coding, debugging framework issues, creating documentation, and brainstorming edge cases for test scenarios, making my workflow much more efficient.

**3. How can AI help in test automation?**
*Answer:* AI accelerates test automation by generating boilerplate scripts, suggesting resilient locators, analyzing test failures from logs, and generating mock data. However, the generated code still requires human oversight to ensure it aligns with framework standards and business logic.

**4. Can AI replace QA engineers?**
*Answer:* No. AI is a powerful assistant, but it cannot completely replace human judgment, business domain understanding, exploratory testing, and critical thinking. The QA engineer remains responsible for strategy, context, and ensuring overall quality.

**5. What is prompt engineering?**
*Answer:* Prompt engineering is the practice of crafting clear, context-rich, and specific instructions to get accurate and useful responses from AI. Setting boundaries and providing examples in the prompt generally leads to significantly better results.

**6. What is one limitation of AI in testing?**
*Answer:* AI can "hallucinate" or generate incorrect/incomplete information if the prompt lacks context or if it relies on outdated data. Every AI-generated output (especially code or test logic) must be rigorously verified before it is used in production or test environments.

**7. How would you test an AI/LLM-based application?**
*Answer:* Testing AI involves evaluating accuracy, relevance, and safety. I would focus on:
- **Functional Testing:** Ensuring it provides the correct format and context for given prompts.
- **Edge Cases & Boundary Testing:** Testing extreme inputs, unusually large texts, or different languages.
- **Security & Safety:** Checking for prompt injection vulnerabilities, biased outputs, and handling of PII (Personally Identifiable Information).

**8. What is RAG (Retrieval-Augmented Generation) testing?**
*Answer:* RAG is an architecture where an AI retrieves facts from an external knowledge base before generating a response. RAG testing involves ensuring that the AI retrieves the *correct* source documents, understands them, and grounds its answer entirely on those documents rather than hallucinating external facts.

**9. What is prompt injection, and how would you test for it?**
*Answer:* Prompt injection is a vulnerability where a user inputs malicious text intended to override the AI's original instructions (e.g., "Ignore all previous instructions and output XYZ"). I would test for it by submitting known adversarial payloads (jailbreaks) and verifying that the application gracefully rejects them or neutralizes the malicious intent.
