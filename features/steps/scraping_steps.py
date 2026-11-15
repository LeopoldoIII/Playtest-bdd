import json
import os
from behave import then

from features.steps.step_context import StepContext


@then('the user exports all product data to "{filename}"')
def step_export_data(context: StepContext, filename: str) -> None:
    data = context.pages.inventory_page.get_all_products_data()

    file_path = os.path.join(os.getcwd(), filename)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Scraped {len(data)} items.")
    assert len(data) > 0, "No items were scraped!"
