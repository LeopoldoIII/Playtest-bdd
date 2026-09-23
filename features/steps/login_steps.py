import os
from behave import given, when, then
from playwright.sync_api import expect

@given('the user is on the login page')
def step_open_login_page(context):
    # Try to get URL from .env first, fallback to config
    url = os.getenv('BASE_URL', context.config_data.get('base_url'))
    context.pages.login_page.navigate(url)

@when('the user enters "{username}" and "{password}"')
def step_enter_credentials(context, username, password):
    context.pages.login_page.login(username, password)

@when('the user enters valid credentials')
def step_enter_valid_credentials(context):
    username = os.getenv('STANDARD_USER', 'standard_user')
    password = os.getenv('SECRET_PASSWORD', 'secret_sauce')
    context.pages.login_page.login(username, password)

@then('the user should be redirected to the inventory page')
def step_verify_redirect(context):
    import re
    # Web-First Assertion instead of just python assert
    # We wait for the URL to contain inventory.html
    expect(context.page).to_have_url(re.compile(".*inventory.html"))
    context.logger.info("Successfully redirected to inventory page")

@then('an error message "{message}" is displayed')
def step_verify_error(context, message):
    error_text = context.pages.login_page.get_error_message()
    assert message in error_text, f"Expected error '{message}' not found in '{error_text}'"
