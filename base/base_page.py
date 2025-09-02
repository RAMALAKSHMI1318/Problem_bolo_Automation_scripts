from playwright.sync_api import Page
from config import BASE_URL, ARTIFACTS_DIR
import os
import time

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str = "", retries: int = 3):
        """Navigate to BASE_URL + path with retry logic"""
        url = BASE_URL.rstrip("/") + "/" + path.lstrip("/")
        for attempt in range(retries):
            try:
                self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
                return
            except Exception as e:
                if attempt == retries - 1:
                    raise
                time.sleep(2)

    def take_screenshot(self, name: str = None):
        """Take screenshot and save in ARTIFACTS_DIR"""
        if not os.path.exists(ARTIFACTS_DIR):
            os.makedirs(ARTIFACTS_DIR)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png" if name else f"screenshot_{timestamp}.png"
        path = os.path.join(ARTIFACTS_DIR, filename)
        self.page.screenshot(path=path)
        print(f"Screenshot saved: {path}")
        return path
