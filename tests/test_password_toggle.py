import pytest
import pandas as pd
import re
import os
from pages.password_toggle_page import PasswordTogglePage
from pytest_html import extras
from config import CSV_FILE

# ------------------ LOAD CSV ------------------
test_data_df = pd.read_csv(CSV_FILE, engine="python")

# Filter rows by TC ID
auth07_df = test_data_df[test_data_df['TC ID'] == 'AUTH07']
auth07_data = auth07_df.to_dict(orient="records")

auth08_df = test_data_df[test_data_df['TC ID'] == 'AUTH08']
auth08_data = auth08_df.to_dict(orient="records")

auth09_df = test_data_df[test_data_df['TC ID'] == 'AUTH09']
auth09_data = auth09_df.to_dict(orient="records")


# ------------------ TEST CASE AUTH07 ------------------
@pytest.mark.parametrize("tc_index,tc", [(0, auth07_data[0])])
def test_auth07_click_login_tab(page, tc_index, tc, request):
    """AUTH07: Click Login/Signin tab."""
    password_page = PasswordTogglePage(page)
    test_passed = False
    error_msg = ""
    expected_result = tc.get("Expected Result", "N/A")

    try:
        password_page.navigate()
        password_page.click_login_tab()
        test_passed = True

    except Exception as e:
        error_msg = str(e)
        if not os.path.exists("reports"):
            os.makedirs("reports")
        screenshot_path = os.path.join("reports", f"{tc['TC ID']}_failure.png")
        password_page.take_screenshot(screenshot_path)
        if hasattr(request.config, "_html"):
            request.config._html.extra.append(extras.image(screenshot_path))
            request.config._html.extra.append(extras.text(f"{tc['TC ID']} Failed: {error_msg}"))

    finally:
        last_index = auth07_df.index[0]
        if test_passed:
            test_data_df.at[last_index, "Status"] = "Passed"
            test_data_df.at[last_index, "Remarks"] = expected_result
        else:
            test_data_df.at[last_index, "Status"] = "Failed"
            test_data_df.at[last_index, "Remarks"] = f"Expected: {expected_result} | Actual: {error_msg}"

        try:
            test_data_df.to_csv(CSV_FILE, index=False)
        except PermissionError:
            temp_csv = CSV_FILE.replace(".csv", "_temp.csv")
            test_data_df.to_csv(temp_csv, index=False)

    if not test_passed:
        pytest.fail(f"{tc['TC ID']} Failed - {error_msg}")


# ------------------ TEST CASE AUTH08 ------------------
@pytest.mark.parametrize("tc_index,tc", [(0, auth08_data[0])])
def test_auth08_forgot_password(page, tc_index, tc, request):
    """AUTH08: Click Forgot Password after Login/Signin tab."""
    password_page = PasswordTogglePage(page)
    test_passed = False
    error_msg = ""
    expected_result = tc.get("Expected Result", "N/A")

    try:
        password_page.navigate()
        password_page.click_login_tab()
        page = password_page.page  # access underlying Playwright page
        page.get_by_role("button", name="Forgot Password?").click()
        test_passed = True

    except Exception as e:
        error_msg = str(e)
        if not os.path.exists("reports"):
            os.makedirs("reports")
        screenshot_path = os.path.join("reports", f"{tc['TC ID']}_failure.png")
        password_page.take_screenshot(screenshot_path)
        if hasattr(request.config, "_html"):
            request.config._html.extra.append(extras.image(screenshot_path))
            request.config._html.extra.append(extras.text(f"{tc['TC ID']} Failed: {error_msg}"))

    finally:
        last_index = auth08_df.index[0]
        if test_passed:
            test_data_df.at[last_index, "Status"] = "Passed"
            test_data_df.at[last_index, "Remarks"] = expected_result
        else:
            test_data_df.at[last_index, "Status"] = "Failed"
            test_data_df.at[last_index, "Remarks"] = f"Expected: {expected_result} | Actual: {error_msg}"

        try:
            test_data_df.to_csv(CSV_FILE, index=False)
        except PermissionError:
            temp_csv = CSV_FILE.replace(".csv", "_temp.csv")
            test_data_df.to_csv(temp_csv, index=False)

    if not test_passed:
        pytest.fail(f"{tc['TC ID']} Failed - {error_msg}")


# ------------------ TEST CASE AUTH09 ------------------
@pytest.mark.parametrize("tc_index,tc", [(0, auth09_data[0])])
def test_auth09_password_toggle(page, tc_index, tc, request):
    """AUTH09: Verify password toggle functionality after Login/Signin tab clicked."""
    password_page = PasswordTogglePage(page)
    test_passed = False
    error_msg = ""
    expected_result = tc.get("Expected Result", "N/A")

    try:
        password_page.navigate()
        password_page.click_login_tab()  # Ensure login tab is active

        # Extract password from Test Data
        test_data_str = str(tc.get("Test Data", ""))
        password_match = re.search(r"Password:\s*([^\s]+)", test_data_str)
        password = password_match.group(1) if password_match else ""

        result = password_page.perform_password_toggle_test(password)
        if not result:
            raise Exception("Password toggle failed")

        test_passed = True

    except Exception as e:
        error_msg = str(e)
        if not os.path.exists("reports"):
            os.makedirs("reports")
        screenshot_path = os.path.join("reports", f"{tc['TC ID']}_failure.png")
        password_page.take_screenshot(screenshot_path)
        if hasattr(request.config, "_html"):
            request.config._html.extra.append(extras.image(screenshot_path))
            request.config._html.extra.append(extras.text(f"{tc['TC ID']} Failed: {error_msg}"))

    finally:
        last_index = auth09_df.index[0]
        if test_passed:
            test_data_df.at[last_index, "Status"] = "Passed"
            test_data_df.at[last_index, "Remarks"] = expected_result
        else:
            test_data_df.at[last_index, "Status"] = "Failed"
            test_data_df.at[last_index, "Remarks"] = f"Expected: {expected_result} | Actual: {error_msg}"

        try:
            test_data_df.to_csv(CSV_FILE, index=False)
        except PermissionError:
            temp_csv = CSV_FILE.replace(".csv", "_temp.csv")
            test_data_df.to_csv(temp_csv, index=False)

    if not test_passed:
        pytest.fail(f"{tc['TC ID']} Failed - {error_msg}")
