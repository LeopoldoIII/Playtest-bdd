import os
import allure
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from pages.page_manager import PageManager
from utils.config_loader import ConfigLoader
from utils.logger import Logger

# Load environment variables from .env file
load_dotenv()

def before_all(context):
    # Setup Logger
    context.logger = Logger.setup_logger()
    context.logger.info("Initializing Test Suite")

    context.config_data = ConfigLoader.get_config()
    context.playwright = sync_playwright().start()

    browser_type = context.config_data.get('browser', 'chromium')
    headless_mode = context.config_data.get('headless', False)

    context.logger.info(f"Launching browser: {browser_type}, Headless: {headless_mode}")

    if browser_type == 'firefox':
        context.browser = context.playwright.firefox.launch(headless=headless_mode)
    elif browser_type == 'webkit':
        context.browser = context.playwright.webkit.launch(headless=headless_mode)
    else:
        context.browser = context.playwright.chromium.launch(headless=headless_mode)


def before_scenario(context, scenario):
    context.logger.info(f"Starting scenario: {scenario.name}")
    
    # Create a new browser context. This is Playwright's equivalent to an incognito window.
    # It allows for independent sessions per scenario.
    context.browser_context = context.browser.new_context()
    
    # Start tracing for this scenario
    context.browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)

    # Open a new page inside the context
    context.page = context.browser_context.new_page()

    # Page Manager initialization
    context.pages = PageManager(context.page)


def after_step(context, step):
    if step.status == "failed":
        context.logger.error(f"Step failed: {step.name}")
        # Attach screenshot to Allure report on failure
        try:
            screenshot_bytes = context.page.screenshot(full_page=True)
            allure.attach(
                screenshot_bytes,
                name=f"Screenshot_{step.name}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            context.logger.error(f"Failed to take screenshot: {e}")

def after_scenario(context, scenario):
    context.logger.info(f"Ending scenario: {scenario.name} | Status: {scenario.status}")
    
    # Stop tracing and save it if the test failed
    if scenario.status == "failed":
        trace_path = f"logs/trace_{scenario.name.replace(' ', '_')}.zip"
        context.browser_context.tracing.stop(path=trace_path)
        context.logger.info(f"Saved trace to {trace_path}")
    else:
        context.browser_context.tracing.stop()

    context.page.close()
    context.browser_context.close()


def after_all(context):
    context.logger.info("Test Suite Completed, closing browser.")
    context.browser.close()
    context.playwright.stop()
