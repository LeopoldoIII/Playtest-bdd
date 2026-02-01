from playwright.sync_api import sync_playwright

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.config_loader import ConfigLoader


def before_all(context):

    context.config_data = ConfigLoader.get_config()
    context.playwright = sync_playwright().start()

    browser_type = context.config_data.get('browser', 'chromium')
    headless_mode = context.config_data.get('headless', False)

    if browser_type == 'firefox':
        context.browser = context.playwright.firefox.launch(headless=headless_mode)
    elif browser_type == 'webkit':
        context.browser = context.playwright.webkit.launch(headless=headless_mode)
    else:
        context.browser = context.playwright.chromium.launch(headless=headless_mode)


def before_scenario(context, scenario):
    """Se ejecuta antes de cada Scenario. Crea una página nueva."""
    context.page = context.browser.new_page()

    # Inicializamos los Page Objects y los guardamos en el contexto
    context.login_page = LoginPage(context.page)
    context.inventory_page = InventoryPage(context.page)


def after_scenario(context, scenario):
    """Se ejecuta al final de cada Scenario. Cierra la página."""
    context.page.close()


def after_all(context):
    """Cierra el navegador y Playwright al final de todo."""
    context.browser.close()
    context.playwright.stop()