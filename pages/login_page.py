from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        
        # Locators (Using Playwright's user-facing locators when possible)
        # Instead of generic CSS, we can use get_by_test_id if the data-test attribute is configured,
        # or we keep CSS but we wrap it in a variable.
        self.username_input = "[data-test='username']"
        self.password_input = "[data-test='password']"
        self.login_button = "[data-test='login-button']"
        self.error_message = "[data-test='error']"

    # Actions
    def login(self, username, password):
        self.logger.info("Attempting to login")
        # Using the BasePage wrapper methods
        self.fill(self.username_input, username, name="Username Input")
        self.fill(self.password_input, password, name="Password Input")
        self.click(self.login_button, name="Login Button")

    def get_error_message(self):
        # We can still use the direct locator if we need inner_text directly,
        # but we wait for it to be visible first just in case.
        self.wait_for_element_visible(self.error_message)
        error_text = self.page.locator(self.error_message).inner_text()
        self.logger.info(f"Error message displayed: '{error_text}'")
        return error_text