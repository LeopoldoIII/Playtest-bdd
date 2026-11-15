from behave import given, when, then

from features.steps.step_context import StepContext


@when('the user adds "{item_name}" to the cart')
def add_item(context: StepContext, item_name: str) -> None:
    context.pages.inventory_page.add_product_by_name(item_name)


@then('the "{product_name}" button changes to "{expected_text}"')
def verify_button_specific(
    context: StepContext, product_name: str, expected_text: str
) -> None:
    context.pages.inventory_page.verify_remove_button(product_name, expected_text)


@then('the shop icon changes to "{count}"')
def verify_cart_badge_count(context: StepContext, count: str) -> None:
    context.pages.inventory_page.verify_cart_badge(count)
