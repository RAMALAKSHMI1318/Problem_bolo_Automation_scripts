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

def test_auth01_valid_login(page: Page, request):
    """AUTH01 - Valid Login with Email and Password"""

    tcid = "AUTH01"
    tc_row = test_data_df[test_data_df['TC ID'] == tcid].iloc[0]
    expected_result = tc_row["Expected Result"]

   
    test_data_str = str(tc_row.get("Test Data", ""))
    email_match = re.search(r"Email:\s*([^\s]+)", test_data_str)
    password_match = re.search(r"Password:\s*([^\s]+)", test_data_str)

    email = email_match.group(1) if email_match else ""
    password = password_match.group(1) if password_match else ""

    login_page = LoginPage(page)

    try:
       
        login_page.navigate("login")


        login_page.login(email, password)

        update_csv_and_report(login_page, request, tcid, expected_result, passed=True)

    except Exception as e:

        update_csv_and_report(
            login_page,
            request,
            tcid,
            expected_result,
            passed=False,
            error=str(e)
        )
        pytest.fail(f"{tcid} Exception: {str(e)}")

def test_auth02_invalid_password(page: Page, request):
    """AUTH02 - Invalid Login with Wrong Password"""

    tcid = "AUTH02"
    tc_row = test_data_df[test_data_df['TC ID'] == tcid].iloc[0]
    expected_result = tc_row["Expected Result"]

    
    test_data_str = str(tc_row.get("Test Data", ""))
    email_match = re.search(r"Email:\s*([^\s]+)", test_data_str)
    password_match = re.search(r"Password:\s*([^\s]+)", test_data_str)

    email = email_match.group(1) if email_match else ""
    password = password_match.group(1) if password_match else ""

    login_page = LoginPage(page)

    try:

        login_page.navigate("login")

        login_page.input_email.fill(email)
        login_page.input_password.fill(password)
        login_page.btn_next.click()

        expect(login_page.error_message).to_have_text(
            "Invalid Credentials, Please Check Email or Password",
            timeout=5000
        )

     
        update_csv_and_report(login_page, request, tcid, expected_result, passed=True)

    except Exception as e:
        
        update_csv_and_report(
            login_page,
            request,
            tcid,
            expected_result,
            passed=False,
            error=str(e)
        )
        pytest.fail(f"{tcid} Exception: {str(e)}")
def test_auth03_invalid_nonexistent_email(page: Page, request):
    """AUTH03 - Invalid Login with Non-existent Email"""

    tcid = "AUTH03"
    tc_row = test_data_df[test_data_df['TC ID'] == tcid].iloc[0]
    expected_result = tc_row["Expected Result"]

   
    test_data_str = str(tc_row.get("Test Data", ""))
    email_match = re.search(r"Email:\s*([^\s]+)", test_data_str)
    password_match = re.search(r"Password:\s*([^\s]+)", test_data_str)

    email = email_match.group(1) if email_match else ""
    password = password_match.group(1) if password_match else ""

    login_page = LoginPage(page)

    try:
       
        login_page.navigate("login")

        
        login_page.input_email.fill(email)
        login_page.input_password.fill(password)

       
        login_page.btn_next.click()

     
        expect(login_page.error_message).to_have_text(
            "Invalid Credentials, Please Check Email or Password",
            timeout=5000
        )
        update_csv_and_report(login_page, request, tcid, expected_result, passed=True)

    except Exception as e:
        update_csv_and_report(
            login_page,
            request,
            tcid,
            expected_result,
            passed=False,
            error=str(e)
        )
        pytest.fail(f"{tcid} Exception: {str(e)}")

def test_auth04_empty_email_field(page: Page, request):
    """AUTH04 - Empty Email Field Validation"""

    tcid = "AUTH04"
    tc_row = test_data_df[test_data_df['TC ID'] == tcid].iloc[0]
    expected_result = tc_row["Expected Result"]

   
    test_data_str = str(tc_row.get("Test Data", ""))
    password_match = re.search(r"Password:\s*([^\s]+)", test_data_str)
    password = password_match.group(1) if password_match else ""

    login_page = LoginPage(page)

    try:
       
        login_page.navigate("login")
        login_page.input_email.fill("")
        login_page.input_password.fill(password)
        assert not login_page.btn_next.is_enabled(), "Next button should be disabled when email is empty"
        update_csv_and_report(login_page, request, tcid, expected_result, passed=True)

    except Exception as e:
        update_csv_and_report(
            login_page,
            request,
            tcid,
            expected_result,
            passed=False,
            error=str(e)
        )
        pytest.fail(f"{tcid} Exception: {str(e)}")

def test_auth05_empty_password_field(page: Page, request):
    """AUTH05 - Empty Password Field Validation"""

    tcid = "AUTH05"
    tc_row = test_data_df[test_data_df['TC ID'] == tcid].iloc[0]
    expected_result = tc_row["Expected Result"]

    
    test_data_str = str(tc_row.get("Test Data", ""))
    email_match = re.search(r"Email:\s*([^\s]+)", test_data_str)
    email = email_match.group(1) if email_match else ""

    login_page = LoginPage(page)

    try:
        login_page.navigate("login")
        login_page.input_email.fill(email)
        login_page.input_password.fill("")
        assert not login_page.btn_next.is_enabled(), "Next button should be disabled when password is empty"

        update_csv_and_report(login_page, request, tcid, expected_result, passed=True)

    except Exception as e:
       
        update_csv_and_report(
            login_page,
            request,
            tcid,
            expected_result,
            passed=False,
            error=str(e)
        )
        pytest.fail(f"{tcid} Exception: {str(e)}")

def test_auth06_invalid_email_format(page: Page, request):
    """AUTH06 - Invalid Email Format Validation"""

    tcid = "AUTH06"
    tc_row = test_data_df[test_data_df['TC ID'] == tcid].iloc[0]
    expected_result = tc_row["Expected Result"]


    test_data_str = str(tc_row.get("Test Data", ""))
    email_match = re.search(r"Email:\s*([^\s]+)", test_data_str)
    password_match = re.search(r"Password:\s*([^\s]+)", test_data_str)

    email = email_match.group(1) if email_match else ""
    password = password_match.group(1) if password_match else ""

    login_page = LoginPage(page)

    try:
      
        login_page.navigate("login")

        login_page.input_email.fill(email)

        login_page.input_password.fill(password)

        login_page.btn_next.click()

        expect(login_page.error_message).to_have_text(
            "Invalid Credentials, Please Check Email or Password",
            timeout=5000
        )


        update_csv_and_report(login_page, request, tcid, expected_result, passed=True)

    except Exception as e:
 
        update_csv_and_report(
            login_page,
            request,
            tcid,
            expected_result,
            passed=False,
            error=str(e)
        )
        pytest.fail(f"{tcid} Exception: {str(e)}")

