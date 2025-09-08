import time
import pytest
import pandas as pd
import re
import os
from pages.password_toggle_page import PasswordTogglePage
from pages.login_page import LoginPage
from pytest_html import extras
from config import CSV_FILE
from playwright.sync_api import Page, expect



# ------------------ LOAD CSV ------------------
test_data_df = pd.read_csv(CSV_FILE, engine="python")


def update_csv_and_report(page_obj, request, tcid, expected, passed, error=""):
    """Helper to update CSV + attach screenshot if failed."""
    last_index = test_data_df[test_data_df['TC ID'] == tcid].index[0]
    if passed:
        test_data_df.at[last_index, "Status"] = "Passed"
        test_data_df.at[last_index, "Remarks"] = expected
    else:
        test_data_df.at[last_index, "Status"] = "Failed"
        test_data_df.at[last_index, "Remarks"] = f"Expected: {expected} | Actual: {error}"

        # Screenshot for failed step
        if not os.path.exists("reports"):
            os.makedirs("reports")
        screenshot_path = os.path.join("reports", f"{tcid}_failure.png")
        page_obj.take_screenshot(screenshot_path)

        if hasattr(request.config, "_html"):
            request.config._html.extra.append(extras.image(screenshot_path))
            request.config._html.extra.append(extras.text(f"{tcid} Failed: {error}"))

    try:
        test_data_df.to_csv(CSV_FILE, index=False)
    except PermissionError:
        temp_csv = CSV_FILE.replace(".csv", "_temp.csv")
        test_data_df.to_csv(temp_csv, index=False)


# ------------------ AUTH07 ------------------
def test_auth07_login_tab(page, request):
    row = test_data_df[test_data_df['TC ID'] == 'AUTH07'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")
    password_page = PasswordTogglePage(page)

    try:
        password_page.navigate()
        password_page.click_login_tab()
        update_csv_and_report(password_page, request, "AUTH07", expected, True)
    except Exception as e:
        update_csv_and_report(password_page, request, "AUTH07", expected, False, str(e))
        pytest.fail("AUTH07 failed")

# ------------------ AUTH09 ------------------
def test_auth09_password_toggle(page, request):
    row = test_data_df[test_data_df['TC ID'] == 'AUTH09'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))
    password_match = re.search(r"Password:\s*([^\s]+)", test_data_str)
    password = password_match.group(1) if password_match else ""

    password_page = PasswordTogglePage(page)

    try:
        password_page.navigate()
        if password_page.perform_password_toggle_test(password):
            update_csv_and_report(password_page, request, "AUTH09", expected, True)
        else:
            update_csv_and_report(password_page, request, "AUTH09", expected, False, "Toggle did not work")
            pytest.fail("AUTH09 failed")
    except Exception as e:
        update_csv_and_report(password_page, request, "AUTH09", expected, False, str(e))
        pytest.fail("AUTH09 failed")


# ------------------ AUTH10 ------------------
def test_auth10_first_next(page, request):
    row = test_data_df[test_data_df['TC ID'] == 'AUTH10'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))
    email, password = "", ""
    if "Email:" in test_data_str:
        email = test_data_str.split("Email:")[1].split(",")[0].strip()
    if "Password:" in test_data_str:
        password = test_data_str.split("Password:")[1].strip()

    login_page = LoginPage(page)

    try:
        login_page.navigate()
        login_page.tab_login.click()
        login_page.input_email.fill(email)
        login_page.input_password.fill(password)
        login_page.btn_next.click()
        update_csv_and_report(login_page, request, "AUTH10", expected, True)
    except Exception as e:
        update_csv_and_report(login_page, request, "AUTH10", expected, False, str(e))
        pytest.fail("AUTH10 failed")


# ------------------ AUTH11 ------------------
def test_auth11_verify_email_in_otp_tab(page, request):
    row = test_data_df[test_data_df['TC ID'] == 'AUTH11'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # Extract email from Test Data
    email = ""
    if "Email:" in test_data_str:
        email = test_data_str.split("Email:")[1].strip()

    login_page = LoginPage(page)

    try:
        # OTP tab is assumed open after AUTH10
        email_locator = page.get_by_text(email, exact=True)
        assert email_locator.is_visible(), f"Email {email} not visible on OTP tab"
        update_csv_and_report(login_page, request, "AUTH11", expected, True)
    except Exception as e:
        update_csv_and_report(login_page, request, "AUTH11", expected, False, str(e))
        pytest.fail("AUTH11 failed")
        



