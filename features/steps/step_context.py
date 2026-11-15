import logging
from typing import Any, Protocol

from playwright.sync_api import Page
from pages.page_manager import PageManager


class StepContext(Protocol):
    """Describe the attributes exposed by the Behave context to step definitions."""

    page: Page
    pages: PageManager
    config_data: dict[str, Any]
    logger: logging.Logger
