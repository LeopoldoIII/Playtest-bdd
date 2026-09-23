import logging
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger("PlaytestBDD") # Default logger, will be overridden by environment

    def navigate(self, url: str):
        self.logger.info(f"Navigating to {url}")
        self.page.goto(url)

    def get_title(self) -> str:
        return self.page.title()

    # --- ACTION WRAPPERS ---
    def click(self, locator: str, name: str = ""):
        """Safe click with logging and exception handling."""
        action_name = name if name else locator
        self.logger.info(f"Clicking on '{action_name}'")
        try:
            self.page.locator(locator).click()
        except PlaywrightTimeoutError:
            self.logger.error(f"TimeoutError: Could not click on '{action_name}'. Element not found or not clickable.")
            raise

    def fill(self, locator: str, text: str, name: str = ""):
        """Safe fill with logging and exception handling."""
        action_name = name if name else locator
        # We don't log the actual text if it's a password, so we just log the action
        log_text = "***" if "password" in action_name.lower() else text
        self.logger.info(f"Filling '{action_name}' with '{log_text}'")
        try:
            self.page.locator(locator).fill(text)
        except PlaywrightTimeoutError:
            self.logger.error(f"TimeoutError: Could not fill '{action_name}'. Element not found.")
            raise

    # --- EXPLICIT WAITS ---
    def wait_for_element_visible(self, locator: str, timeout: int = 5000):
        """
        Playwright auto-waits, but sometimes you explicitly need to wait for an element
        to be visible before proceeding (e.g. waiting for a loader to disappear).
        """
        self.logger.debug(f"Waiting for '{locator}' to be visible (Timeout: {timeout}ms)")
        self.page.locator(locator).wait_for(state="visible", timeout=timeout)
        
    def wait_for_element_hidden(self, locator: str, timeout: int = 5000):
        """Waits for an element to be hidden or detached."""
        self.logger.debug(f"Waiting for '{locator}' to be hidden (Timeout: {timeout}ms)")
        self.page.locator(locator).wait_for(state="hidden", timeout=timeout)

    # --- STATE CHECKS ---
    def is_visible(self, locator: str, name: str = "") -> bool:
        """Check if an element is visible."""
        action_name = name if name else locator
        self.logger.debug(f"Checking visibility of '{action_name}'")
        return self.page.locator(locator).is_visible()

    def is_enabled(self, locator: str, name: str = "") -> bool:
        """Check if an element is enabled."""
        action_name = name if name else locator
        self.logger.debug(f"Checking if '{action_name}' is enabled")
        return self.page.locator(locator).is_enabled()

    # --- GET DATA ---
    def get_text(self, locator: str, name: str = "") -> str:
        """Get the inner text of an element."""
        action_name = name if name else locator
        self.logger.debug(f"Getting text from '{action_name}'")
        return self.page.locator(locator).inner_text()

    def get_attribute(self, locator: str, attribute: str, name: str = "") -> str:
        """Get the value of a specific attribute of an element."""
        action_name = name if name else locator
        self.logger.debug(f"Getting attribute '{attribute}' from '{action_name}'")
        return self.page.locator(locator).get_attribute(attribute) or ""

    # --- MORE ACTIONS ---
    def hover(self, locator: str, name: str = ""):
        """Hover over an element."""
        action_name = name if name else locator
        self.logger.info(f"Hovering over '{action_name}'")
        try:
            self.page.locator(locator).hover()
        except PlaywrightTimeoutError:
            self.logger.error(f"TimeoutError: Could not hover over '{action_name}'. Element not found.")
            raise

    def select_option(self, locator: str, value: str, name: str = ""):
        """Select an option from a dropdown by value."""
        action_name = name if name else locator
        self.logger.info(f"Selecting option '{value}' in '{action_name}'")
        try:
            self.page.locator(locator).select_option(value)
        except PlaywrightTimeoutError:
            self.logger.error(f"TimeoutError: Could not select option in '{action_name}'. Element not found.")
            raise

    def check(self, locator: str, name: str = ""):
        """Check a checkbox or radio button."""
        action_name = name if name else locator
        self.logger.info(f"Checking '{action_name}'")
        try:
            self.page.locator(locator).check()
        except PlaywrightTimeoutError:
            self.logger.error(f"TimeoutError: Could not check '{action_name}'. Element not found.")
            raise

    def uncheck(self, locator: str, name: str = ""):
        """Uncheck a checkbox."""
        action_name = name if name else locator
        self.logger.info(f"Unchecking '{action_name}'")
        try:
            self.page.locator(locator).uncheck()
        except PlaywrightTimeoutError:
            self.logger.error(f"TimeoutError: Could not uncheck '{action_name}'. Element not found.")
            raise

    def press(self, locator: str, key: str, name: str = ""):
        """Press a keyboard key on an element."""
        action_name = name if name else locator
        self.logger.info(f"Pressing '{key}' on '{action_name}'")
        try:
            self.page.locator(locator).press(key)
        except PlaywrightTimeoutError:
            self.logger.error(f"TimeoutError: Could not press '{key}' on '{action_name}'. Element not found.")
            raise