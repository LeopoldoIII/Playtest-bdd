from playwright.sync_api import Page, expect

class PlaywrightUtils:
    @staticmethod
    def wait_for_network_idle(page: Page, timeout: int = 30000):
        """
        Useful for SPAs. Waits until there are no network connections for at least 500 ms.
        """
        page.wait_for_load_state("networkidle", timeout=timeout)

    @staticmethod
    def check_element_exists_without_waiting(page: Page, selector: str) -> bool:
        """
        Sometimes in Selenium you use find_elements() to check if something exists without crashing.
        In Playwright, you can just check the count.
        """
        return page.locator(selector).count() > 0

    @staticmethod
    def assert_element_visible(page: Page, selector: str, timeout: int = 5000):
        """
        Web-First Assertion example. This replaces WebDriverWait in Selenium.
        It will automatically retry until the element is visible or the timeout is reached.
        """
        expect(page.locator(selector)).to_be_visible(timeout=timeout)

    @staticmethod
    def assert_element_has_text(page: Page, selector: str, text: str, timeout: int = 5000):
        """
        Asserts that an element contains specific text.
        """
        expect(page.locator(selector)).to_have_text(text, timeout=timeout)
