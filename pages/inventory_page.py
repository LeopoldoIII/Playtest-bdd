from pages.base_page import BasePage
from playwright.sync_api import expect


class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Locators
        self.inventory_item_description = page.locator(".inventory_item_description")
        self.inventory_item = page.locator(".inventory_item")
        self.shopping_cart_badge = page.locator(".shopping_cart_badge")

    # Actions
    def add_product_by_name(self, product_name):
        self.inventory_item.filter(has_text=product_name).get_by_role("button", name="Add to cart").click()

    def verify_remove_button(self, product_name, expected_text):
        button = self.inventory_item_description.filter(has_text=product_name).locator("button")
        expect(button).to_have_text(expected_text)

    def verify_cart_badge(self, expected_count):
        expect(self.shopping_cart_badge).to_have_text(expected_count)

    def get_all_products_data(self):

        products_data = []

        all_items = self.inventory_item_description.all()

        for item in all_items:
            title = item.locator(".inventory_item_name").inner_text()
            desc = item.locator(".inventory_item_desc").inner_text()
            price = item.locator(".inventory_item_price").inner_text()

            products_data.append({
                "title": title,
                "description": desc,
                "price": price
            })

        return products_data