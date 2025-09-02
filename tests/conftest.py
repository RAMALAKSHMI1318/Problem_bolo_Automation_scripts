# tests/conftest.py
import pytest
from config import ARTIFACTS_DIR
import os
import time

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take screenshot on test failure"""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            if not os.path.exists(ARTIFACTS_DIR):
                os.makedirs(ARTIFACTS_DIR)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(ARTIFACTS_DIR, f"{item.name}_{timestamp}.png")
            page.screenshot(path=screenshot_path)
            print(f"\nScreenshot saved: {screenshot_path}")
