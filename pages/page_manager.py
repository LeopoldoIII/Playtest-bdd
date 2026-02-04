from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class PageManager:
    def __init__(self, page):
        self.page = page
        self._login_page = None
        self._inventory_page = None

    @property
    def login_page(self):
        if self._login_page is None:
            self._login_page = LoginPage(self.page)
        return self._login_page

    @property
    def inventory_page(self):
        if self._inventory_page is None:
            self._inventory_page = InventoryPage(self.page)
        return self._inventory_page
