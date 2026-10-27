import os
import re
import allure
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from pages.page_manager import PageManager
from utils.config_loader import ConfigLoader
from utils.logger import Logger

# Load environment variables from .env file
load_dotenv()


def _sanitize_filename(name: str) -> str:
    """Sanitize scenario name for filesystem-safe artifact paths."""
    return re.sub(r'[^\w\-_\. ]', '_', name).strip().replace(' ', '_')


def before_all(context):
    """Initializes global test configuration, logging, and Playwright browser instance."""
    context.logger = Logger.setup_logger()
    context.logger.info("Initializing Test Suite")

    context.config_data = ConfigLoader.get_config()
    context.playwright = sync_playwright().start()

    browser_type = os.getenv('BROWSER', context.config_data.get('browser', 'chromium')).lower()
    headless_env = os.getenv('HEADLESS')
    if headless_env is not None:
        headless_mode = headless_env.lower() in ('true', '1', 'yes')
    else:
        headless_mode = context.config_data.get('headless', False)

    launch_args = {"headless": headless_mode}
    context.logger.info(f"Launching browser: {browser_type}, Headless: {headless_mode}")

    if browser_type == 'firefox':
        context.browser = context.playwright.firefox.launch(**launch_args)
    elif browser_type == 'webkit':
        context.browser = context.playwright.webkit.launch(**launch_args)
    else:
        context.browser = context.playwright.chromium.launch(**launch_args)


def before_scenario(context, scenario):
    """Executes before each scenario: creates an isolated browser context, enables tracing, and initializes page."""
    context.logger.info(f"Starting scenario: {scenario.name}")
    context.browser_context = context.browser.new_context()

    # Start tracing to capture actions, DOM snapshots, and screenshots for post-mortem debugging
    context.browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)

    context.page = context.browser_context.new_page()

    # Initialize Page Object Manager
    context.pages = PageManager(context.page)


def after_step(context, step):
    """Executes after each step: logs failures and captures screenshot for Allure report."""
    if step.status == "failed":
        context.logger.error(f"Step failed: {step.name}")
        try:
            screenshot_bytes = context.page.screenshot(full_page=True)
            allure.attach(
                screenshot_bytes,
                name=f"Screenshot_{step.name}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            context.logger.error(f"Failed to take step failure screenshot: {e}")


def after_scenario(context, scenario):
    """Executes after each scenario: captures trace and screenshot on failure, then tears down context."""
    context.logger.info(f"Ending scenario: {scenario.name} | Status: {scenario.status}")
    safe_name = _sanitize_filename(scenario.name)

    if scenario.status == 'failed':
        os.makedirs("reports/screenshots", exist_ok=True)
        os.makedirs("reports/traces", exist_ok=True)
        os.makedirs("logs", exist_ok=True)

        screenshot_path = f"reports/screenshots/{safe_name}.png"
        trace_path = f"reports/traces/{safe_name}.zip"

        try:
            context.page.screenshot(path=screenshot_path)
            context.browser_context.tracing.stop(path=trace_path)
            context.logger.info(f"Saved trace to {trace_path}")
        except Exception as e:
            context.logger.error(f"Failed to save failure artifacts: {e}")
            context.browser_context.tracing.stop()
    else:
        context.browser_context.tracing.stop()

    context.page.close()
    context.browser_context.close()


def after_all(context):
    """Closes the browser and stops Playwright at the end of the test run."""
    context.logger.info("Test Suite Completed, closing browser.")
    context.browser.close()
    context.playwright.stop()
