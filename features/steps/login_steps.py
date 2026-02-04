from behave import given, when, then


@given('the user is on the login page')
def step_open_login_page(context):
    # access to the URL from the config
    url = context.config_data['base_url']
    context.pages.login_page.navigate(url)


@when('the user enters "{username}" and "{password}"')
def step_enter_credentials(context, username, password):
    context.pages.login_page.login(username, password)


@then('the user should be redirected to the inventory page')
def step_verify_redirect(context):
    assert "inventory.html" in context.page.url


@then('an error message "{message}" is displayed')
def step_verify_error(context, message):
    error_text = context.pages.login_page.get_error_message()
    assert message in error_text
