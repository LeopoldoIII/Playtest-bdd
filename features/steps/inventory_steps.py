from behave import given, when, then

@when('the user adds "{item_name}" to the cart')
def add_item(context, item_name):
    context.inventory_page.add_product_by_name(item_name)

@then('the "{product_name}" button changes to "{expected_text}"')
def verify_button_specific(context, product_name, expected_text):
    context.inventory_page.verify_remove_button(product_name, expected_text)