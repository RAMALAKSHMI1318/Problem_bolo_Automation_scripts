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
from pages.forgot_password_page import ForgotPasswordPage


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


def test_fpass01_click_forgot_password(page, request):
    # Get test data for FPASS01 from CSV
    row = test_data_df[test_data_df['TC ID'] == 'FPASS01'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")

    # Create page object
    fp_page = ForgotPasswordPage(page)

    try:
        # Navigate and click login tab
        fp_page.navigate()
        fp_page.click_login_tab()

        # Click Forgot Password button
        fp_page.click_forgot_password_button()

        # If successful, update CSV as Passed
        update_csv_and_report(fp_page, request, "FPASS01", expected, True)

    except Exception as e:
        # If failed, update CSV as Failed and take screenshot
        update_csv_and_report(fp_page, request, "FPASS01", expected, False, str(e))
        pytest.fail("FPASS01 failed")

def test_fpass02_check_forgot_password_title(page, request):
    # Get test data for FPASS02 from CSV
    row = test_data_df[test_data_df['TC ID'] == 'FPASS02'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # Create page object
    fp_page = ForgotPasswordPage(page)

    try:
        # Fresh start: navigate and open Forgot Password modal
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()

        # Directly locate the modal title and assert visibility
        title_locator = page.get_by_text("Forgot Password", exact=True)
        assert title_locator.is_visible(), f"Forgot Password title not visible. Test Data: {test_data_str}"

        # Update CSV as Passed
        update_csv_and_report(fp_page, request, "FPASS02", expected, True)

    except Exception as e:
        # Update CSV as Failed and take screenshot
        update_csv_and_report(fp_page, request, "FPASS02", expected, False, str(e))
        pytest.fail("FPASS02 failed")

def test_fpass03_verify_forgot_password_details(page, request):
    # 🔄 Get test data for FPASS03 from CSV
    row = test_data_df[test_data_df['TC ID'] == 'FPASS03'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # Extract the "Or" text from Test Data column
    or_text = test_data_str.strip() if test_data_str else "Or"

    fp_page = ForgotPasswordPage(page)

    try:
        # Open Forgot Password modal
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()

        # Verify form elements
        assert fp_page.is_mobile_input_visible(), "Mobile input not visible"
        assert fp_page.is_email_input_visible(), "Email input not visible"

        # Verify "Or" separator dynamically from CSV
        or_locator = page.get_by_text(or_text, exact=True)
        assert or_locator.is_visible(), f"'{or_text}' separator not visible"

        # Update CSV as Passed
        update_csv_and_report(fp_page, request, "FPASS03", expected, True)

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS03", expected, False, str(e))
        pytest.fail("FPASS03 failed")

def test_fpass04_enter_mobile_and_click_next(page, request):
    # Get test data for FPASS04 from CSV
    row = test_data_df[test_data_df['TC ID'] == 'FPASS04'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # Extract mobile number from Test Data column (mobile:6476437332)
    mobile_number = ""
    if "mobile:" in test_data_str:
        mobile_number = test_data_str.split("mobile:")[1].strip()

    fp_page = ForgotPasswordPage(page)

    try:
        # Open Forgot Password modal
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()

        # Enter mobile number and click Next
        fp_page.enter_mobile_number(mobile_number)
        fp_page.click_next_button()

        # Update CSV/report as Passed
        update_csv_and_report(fp_page, request, "FPASS04", expected, True)

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS04", expected, False, str(e))
        pytest.fail("FPASS04 failed")

def test_fpass05_enter_email_and_click_next(page, request):
    # Get test data for FPASS05 from CSV
    row = test_data_df[test_data_df['TC ID'] == 'FPASS05'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # Extract email from Test Data column
    email_address = ""
    if "Email:" in test_data_str:
        email_address = test_data_str.split("Email:")[1].strip()

    fp_page = ForgotPasswordPage(page)

    try:
        # Open Forgot Password modal
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()

        # Enter email address
        fp_page.enter_email(email_address)
        # Click Next button
        fp_page.click_next_button()

        # Update CSV/report as Passed
        update_csv_and_report(fp_page, request, "FPASS05", expected, True)

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS05", expected, False, str(e))
        pytest.fail("FPASS05 failed")

def test_fpass06_enter_both_inputs(page, request):
    # Get test data for FPASS06 from CSV
    row = test_data_df[test_data_df['TC ID'] == 'FPASS06'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # Extract mobile and email from Test Data
    mobile_number = ""
    email_address = ""
    for line in test_data_str.splitlines():
        if line.strip().lower().startswith("mobile:"):
            mobile_number = line.split(":", 1)[1].strip()
        elif line.strip().lower().startswith("email:"):
            email_address = line.split(":", 1)[1].strip()

    fp_page = ForgotPasswordPage(page)

    try:
        # Open Forgot Password modal
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()

        # Enter both inputs
        if mobile_number:
            fp_page.enter_mobile_number(mobile_number)
        if email_address:
            fp_page.enter_email(email_address)

        # Optional: verify email takes precedence (if your app sets a flag)
        # flag_locator = page.locator("selector-for-email-precedence-flag")
        # expect(flag_locator).to_have_attribute("data-flag", "true")

        # Click Next button
        fp_page.click_next_button()

        # Update CSV/report as Passed
        update_csv_and_report(fp_page, request, "FPASS06", expected, True)

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS06", expected, False, str(e))
        pytest.fail("FPASS06 failed")

def test_fpass07_next_button_disabled_without_input(page, request):
    # Get test data for FPASS07 from CSV
    row = test_data_df[test_data_df['TC ID'] == 'FPASS07'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # Extract mobile and email from CSV
    mobile_number = ""
    email_address = ""
    parts = test_data_str.split(";")
    for part in parts:
        if "mobile=" in part:
            val = part.split("mobile=")[1].strip().strip("'\"")
            mobile_number = "" if val in ["", "''"] else val
        elif "email=" in part:
            val = part.split("email=")[1].strip().strip("'\"")
            email_address = "" if val in ["", "''"] else val

    fp_page = ForgotPasswordPage(page)

    try:
        # Open Forgot Password modal
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()

        # Enter values (both empty in this test case)
        fp_page.enter_mobile_number(mobile_number)
        fp_page.enter_email(email_address)

        # ✅ Use locator from page object
        next_button = page.locator(fp_page.NEXT_BUTTON_DISABLED).first
        expect(next_button).to_be_disabled()

        update_csv_and_report(fp_page, request, "FPASS07", expected, True)

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS07", expected, False, str(e))
        pytest.fail("FPASS07 failed")

def test_fpass08_otp_tab_navigation(page, request):
    # Get test data for FPASS08 from CSV
    row = test_data_df[test_data_df['TC ID'] == 'FPASS08'].to_dict(orient="records")[0]       
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))  # multi-line input from CSV

    fp_page = ForgotPasswordPage(page)

    try:
        # Open Forgot Password modal
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()

        # Extract mobile and email from CSV
        mobile_number = ""
        email_address = ""
        for line in test_data_str.splitlines():
            if line.strip().lower().startswith("mobile:"):
                mobile_number = line.split(":", 1)[1].strip()
            elif line.strip().lower().startswith("email:"):
                email_address = line.split(":", 1)[1].strip()

        # Enter mobile/email if available
        if mobile_number:
            fp_page.enter_mobile_number(mobile_number)
        if email_address:
            fp_page.enter_email(email_address)

        # Click Next using ForgotPasswordPage method
        fp_page.click_next_button()

        # Wait for OTP input boxes to appear and verify visibility
        otp_inputs = page.locator("input[type='text'][maxlength='1']")
        expect(otp_inputs).to_have_count(4, timeout=5000)  # expecting 4 OTP boxes

        for i in range(4):
            expect(otp_inputs.nth(i)).to_be_visible()
            # Optional: print pre-filled value
            print(f"OTP input {i+1} pre-filled value: {otp_inputs.nth(i).input_value()}")

            # Update CSV/report as Passed
            update_csv_and_report(fp_page, request, "FPASS08", expected, True)

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS08", expected, False, str(e))
        pytest.fail("FPASS08 failed")
# ------------------ FPASS09 ------------------
def test_fpass09_otp_email_display(page, request):
    # Get test data for FPASS09
    rows = test_data_df[test_data_df['TC ID'] == 'FPASS09'].to_dict(orient="records")
    if not rows:
        pytest.skip("FPASS09 test data not found in CSV")
    row = rows[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # Extract real and masked email from CSV
    real_email = ""
    masked_email = ""
    for line in test_data_str.splitlines():
        line_lower = line.strip().lower()
        if line_lower.startswith("email:"):
            real_email = line.split(":", 1)[1].strip()
        elif line_lower.startswith("masked_email:"):
            masked_email = line.split(":", 1)[1].strip()

    fp_page = ForgotPasswordPage(page)

    try:
        # Open Forgot Password modal and enter the real email
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()
        fp_page.enter_email(real_email)
        fp_page.click_next_button()  # Navigate to OTP tab

        # Verify OTP message with masked email is visible
        otp_message = f"Enter OTP sent to {masked_email}"
        otp_message_locator = page.locator("div.field-lbl", has_text=otp_message)
        expect(otp_message_locator).to_be_visible(timeout=5000)

        # Update CSV/report as Passed
        update_csv_and_report(fp_page, request, "FPASS09", expected, True)

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS09", expected, False, str(e))
        pytest.fail("FPASS09 failed")

def test_fpass10_otp_input_validation(page, request):
    # Get test data for FPASS10
    rows = test_data_df[test_data_df['TC ID'] == 'FPASS10'].to_dict(orient="records")
    if not rows:
        pytest.skip("FPASS10 test data not found in CSV")
    row = rows[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # Extract email and OTP from CSV
    real_email = ""
    otp_value = ""
    for line in test_data_str.splitlines():
        line_lower = line.strip().lower()
        if line_lower.startswith("email:"):
            real_email = line.split(":", 1)[1].strip()
        elif line_lower.startswith("otp:"):
            otp_value = line.split(":", 1)[1].strip()

    fp_page = ForgotPasswordPage(page)

    try:
        # -------------------- Step 1: Enter Email --------------------
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()
        fp_page.enter_email(real_email)
        fp_page.click_next_button()  # Navigate to OTP tab

        # -------------------- Step 2: Wait for OTP inputs --------------------
        otp_inputs = page.locator("input[type='text'][maxlength='1']")
        expect(otp_inputs).to_have_count(len(otp_value), timeout=5000)

        # -------------------- Step 3: Clear and overwrite OTP fields repeatedly --------------------
        for i in range(len(otp_value)):
            otp_input = otp_inputs.nth(i)
            # Clear the field multiple times to prevent auto-fill overwriting
            otp_input.fill("")
            otp_input.press("Backspace")
            otp_input.type(otp_value[i])  # Type CSV OTP

        # -------------------- Step 4: Validate allowed characters --------------------
        all_valid = True
        for i, char in enumerate(otp_value):
            entered_char = otp_inputs.nth(i).input_value()
            if not entered_char.isalnum():  # Not A-Z or 0-9
                all_valid = False
                print(f"Invalid character '{entered_char}' was rejected at OTP box {i+1}")
            else:
                print(f"Allowed character '{entered_char}' accepted at OTP box {i+1}")

        # -------------------- Step 5: Update CSV/report --------------------
        update_csv_and_report(fp_page, request, "FPASS10", expected, all_valid)

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS10", expected, False, str(e))
        pytest.fail("FPASS10 failed")

def test_fpass11_otp_autofocus(page, request):
    # Get test data for FPASS11
    rows = test_data_df[test_data_df['TC ID'] == 'FPASS11'].to_dict(orient="records")
    if not rows:
        pytest.skip("FPASS11 test data not found in CSV")
    row = rows[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # Extract email and OTP from CSV
    email = ""
    otp_value = ""
    for line in test_data_str.splitlines():
        line_lower = line.strip().lower()
        if line_lower.startswith("email:"):
            email = line.split(":", 1)[1].strip()
        elif line_lower.startswith("otp:"):
            otp_value = line.split(":", 1)[1].strip()

    fp_page = ForgotPasswordPage(page)

    try:
        # -------------------- Step 1: Enter Email --------------------
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()
        fp_page.enter_email(email)
        fp_page.click_next_button()  # Navigate to OTP tab

        # -------------------- Step 2: Wait for OTP inputs --------------------
        otp_inputs = page.locator("input[type='text'][maxlength='1']")
        expect(otp_inputs).to_have_count(len(otp_value), timeout=5000)

        # -------------------- Step 3: Clear any auto-generated OTP --------------------
        for i in range(len(otp_value)):
            otp_input = otp_inputs.nth(i)
            otp_input.fill("")
            otp_input.press("Backspace")  # ensure field is empty

        # -------------------- Step 4: Enter OTP and check auto-focus --------------------
        autofocus_worked = True
        for i, char in enumerate(otp_value):
            otp_input = otp_inputs.nth(i)
            otp_input.type(char)
            
            entered_char = otp_input.input_value()
            if entered_char.upper() != char.upper():
                autofocus_worked = False
                print(f"OTP box {i+1} value mismatch: expected '{char}', got '{entered_char}'")

            # Check focus moves to next box (except last)
            if i < len(otp_value) - 1:
                active_index = page.evaluate("""
                    () => Array.from(document.querySelectorAll('input[type="text"][maxlength="1"]'))
                          .indexOf(document.activeElement)
                """)
                if active_index != i + 1:
                    autofocus_worked = False
                    print(f"Focus did not move to OTP box {i+2}")

        # -------------------- Step 5: Update CSV/report --------------------
        update_csv_and_report(fp_page, request, "FPASS11", expected, autofocus_worked)

        if not autofocus_worked:
            pytest.fail("FPASS11 failed: OTP auto-focus or value mismatch")

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS11", expected, False, str(e))
        pytest.fail("FPASS11 failed due to exception")

def test_fpass12_otp_backspace_navigation(page, request):
    # Get test data for FPASS12
    rows = test_data_df[test_data_df['TC ID'] == 'FPASS12'].to_dict(orient="records")
    if not rows:
        pytest.skip("FPASS12 test data not found in CSV")
    row = rows[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # Extract email and OTP from CSV
    email = ""
    otp_value = ""
    for line in test_data_str.splitlines():
        if line.strip().lower().startswith("email:"):
            email = line.split(":", 1)[1].strip()
        elif line.strip().lower().startswith("otp:"):
            otp_value = line.split(":", 1)[1].strip()

    fp_page = ForgotPasswordPage(page)

    try:
        # Step 1: Enter Email
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()
        fp_page.enter_email(email)
        fp_page.click_next_button()  # Navigate to OTP tab

        # Step 2: Wait for OTP inputs
        otp_inputs = page.locator("input[type='text'][maxlength='1']")
        expect(otp_inputs).to_have_count(len(otp_value), timeout=5000)

        # Step 3: Clear auto-generated OTP
        for i in range(len(otp_value)):
            otp_inputs.nth(i).fill("")

        # Step 4: Enter OTP from CSV
        for i, char in enumerate(otp_value):
            otp_inputs.nth(i).type(char)

        # Step 5: Backspace Navigation
        backspace_worked = True
        for i in range(len(otp_value)-1, 0, -1):  # Start from last OTP box
            otp_input = otp_inputs.nth(i)
            otp_input.fill("")             # Clear the box
            page.wait_for_timeout(100)     # Small delay for UI to register
            otp_input.press("Backspace")   # Press Backspace
            otp_input.press("Backspace") 

            # Check if focus moved to previous box
            active_index = page.evaluate("""
                () => Array.from(document.querySelectorAll('input[type="text"][maxlength="1"]'))
                      .indexOf(document.activeElement)
            """)
            if active_index != i - 1:
                backspace_worked = False
                print(f"Backspace on OTP box {i+1} did not move focus to box {i}")

        # Step 6: Update CSV/report
        update_csv_and_report(fp_page, request, "FPASS12", expected, backspace_worked)

        if not backspace_worked:
            pytest.fail("FPASS12 failed: Backspace navigation did not work correctly")

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS12", expected, False, str(e))
        pytest.fail("FPASS12 failed")


def test_fpass13_next_button_state(page, request):
    # Get test data for FPASS13
    rows = test_data_df[test_data_df['TC ID'] == 'FPASS13'].to_dict(orient="records")
    if not rows:
        pytest.skip("FPASS13 test data not found in CSV")
    row = rows[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # Extract email and OTP from CSV
    real_email = ""
    otp_value = ""
    for line in test_data_str.splitlines():
        line_lower = line.strip().lower()
        if line_lower.startswith("email:"):
            real_email = line.split(":", 1)[1].strip()
        elif line_lower.startswith("otp:"):
            otp_value = line.split(":", 1)[1].strip()

    fp_page = ForgotPasswordPage(page)

    try:
        # -------------------- Step 1: Enter Email --------------------
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()
        fp_page.enter_email(real_email)
        fp_page.click_next_button()  # Navigate to OTP tab

        # -------------------- Step 2: Wait for OTP inputs --------------------
        otp_inputs = page.locator("input[type='text'][maxlength='1']")
        expect(otp_inputs).to_have_count(4, timeout=5000)  # Always 4 OTP boxes

        # -------------------- Step 3: Clear all OTP boxes --------------------
        for i in range(4):
            otp_inputs.nth(i).fill("")
            otp_inputs.nth(i).press("Backspace")

        # -------------------- Step 4: Enter only first 3 OTP digits --------------------
        for i in range(3):
            otp_inputs.nth(i).type(otp_value[i])

        # ✅ Leave 4th box empty

        # Step 5: Verify Next button is disabled
        if fp_page.is_next_button_disabled():
            print("✅ Next button is disabled with incomplete OTP → Test Passed")
            update_csv_and_report(fp_page, request, "FPASS13", expected, True)
        else:
            print("❌ Next button is enabled with incomplete OTP → Test Failed")
            update_csv_and_report(fp_page, request, "FPASS13", expected, False, "Next button enabled")


    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS13", expected, False, str(e))
        pytest.fail("FPASS13 failed")

def test_fpass14_otp_countdown_timer(page, request):
    # Get test data for FPASS14
    rows = test_data_df[test_data_df['TC ID'] == 'FPASS14'].to_dict(orient="records")
    if not rows:
        pytest.skip("FPASS14 test data not found in CSV")
    row = rows[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # Extract email from CSV
    email = ""
    for line in test_data_str.splitlines():
        if line.strip().lower().startswith("email:"):
            email = line.split(":", 1)[1].strip()

    fp_page = ForgotPasswordPage(page)

    try:
        # Step 1: Navigate to Forgot Password
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()
        fp_page.enter_email(email)
        fp_page.click_next_button()  # Navigate to OTP tab

        # Step 2: Wait for OTP tab to load
        otp_inputs = page.locator("input[type='text'][maxlength='1']")
        expect(otp_inputs).to_have_count(4, timeout=5000)

        # Step 3: Check that Resend button stays disabled for 20 seconds
        import time
        test_passed = True
        for second in range(20):
            is_disabled = fp_page.page.locator(fp_page.RESEND_BUTTON).get_attribute("disabled") is not None
            print(f"Second {second+1}: Resend button disabled = {is_disabled}")
            if not is_disabled:
                test_passed = False
                print("❌ Resend button enabled before 20 seconds → Test Failed")
                break
            time.sleep(1)

        # Step 4: Update CSV/report
        if test_passed:
            print("✅ Resend button stayed disabled for 20 seconds → Test Passed")
            update_csv_and_report(fp_page, request, "FPASS14", expected, True)
        else:
            update_csv_and_report(fp_page, request, "FPASS14", expected, False, "Resend enabled too early")

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS14", expected, False, str(e))
        pytest.fail("FPASS14 failed")

def test_fpass15_resend_otp_enabled_after_countdown(page, request):
    # Get test data for FPASS15
    rows = test_data_df[test_data_df['TC ID'] == 'FPASS15'].to_dict(orient="records")
    if not rows:
        pytest.skip("FPASS15 test data not found in CSV")
    row = rows[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # Extract email from CSV
    email = ""
    for line in test_data_str.splitlines():
        if line.strip().lower().startswith("email:"):
            email = line.split(":", 1)[1].strip()

    fp_page = ForgotPasswordPage(page)

    try:
        # Step 1: Navigate to Forgot Password
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()
        fp_page.enter_email(email)
        fp_page.click_next_button()  # Navigate to OTP tab

        # Step 2: Wait for OTP tab to load
        otp_inputs = page.locator("input[type='text'][maxlength='1']")
        expect(otp_inputs).to_have_count(4, timeout=5000)

        # Step 3: Wait for countdown to complete (20 sec)
        import time
        time.sleep(20)  # Wait for timer to reach 0

        # Step 4: Check if Resend OTP button is enabled
        if fp_page.is_resend_enabled():
            print("✅ Resend OTP button enabled after countdown → Test Passed")
            update_csv_and_report(fp_page, request, "FPASS15", expected, True)
        else:
            print("❌ Resend OTP button still disabled → Test Failed")
            update_csv_and_report(fp_page, request, "FPASS15", expected, False, "Resend OTP button disabled")

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS15", expected, False, str(e))
        pytest.fail("FPASS15 failed")

def test_fpass16_back_button(page, request):
    # Get test data for FPASS16
    rows = test_data_df[test_data_df['TC ID'] == 'FPASS16'].to_dict(orient="records")
    if not rows:
        pytest.skip("FPASS16 test data not found in CSV")
    row = rows[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # Extract email from CSV
    email = ""
    for line in test_data_str.splitlines():
        if line.strip().lower().startswith("email:"):
            email = line.split(":", 1)[1].strip()

    fp_page = ForgotPasswordPage(page)

    try:
        # Step 1: Navigate to Forgot Password and go to OTP tab
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()
        fp_page.enter_email(email)
        fp_page.click_next_button()  # Navigate to OTP tab
        fp_page.click_next_button()

        # Step 2: Click Back button from OTP tab
        fp_page.click_back_button()

        # Step 3: Verify that the 4 OTP input boxes are visible
        otp_inputs = page.locator("input[type='text'][maxlength='1']")
        expect(otp_inputs).to_have_count(4, timeout=5000)

        # ✅ Update CSV/report as Passed
        update_csv_and_report(fp_page, request, "FPASS16", expected, True)
        print("✅ Back button clicked and OTP input boxes are visible → Test Passed")

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS16", expected, False, str(e))
        pytest.fail("FPASS16 failed")


def test_fpass17_set_new_password_tab(page, request):
    rows = test_data_df[test_data_df['TC ID'] == 'FPASS17'].to_dict(orient="records")
    if not rows:
        pytest.skip("FPASS17 test data not found in CSV")
    row = rows[0]
    expected = row.get("Expected Result", "N/A")
    email = next((line.split(":", 1)[1].strip() for line in str(row.get("Test Data", "")).splitlines() if line.lower().startswith("email:")), "")

    fp_page = ForgotPasswordPage(page)

    try:
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()
        fp_page.enter_email(email)

        fp_page.click_next_button()  # OTP tab
        fp_page.click_next_button()  # Set New Password tab

        # Verify using locator from page class
        if page.locator(ForgotPasswordPage.NEW_PASSWORD_TAB_TEXT).is_visible():
            print("✅ Set New Password tab displayed → Test Passed")
            update_csv_and_report(fp_page, request, "FPASS17", expected, True)
        else:
            print("❌ Set New Password tab not displayed → Test Failed")
            update_csv_and_report(fp_page, request, "FPASS17", expected, False, "Set New Password tab not visible")

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS17", expected, False, str(e))
        pytest.fail("FPASS17 failed")


def test_fpass18_password_input(page, request):
    # Get test data for FPASS18
    rows = test_data_df[test_data_df['TC ID'] == 'FPASS18'].to_dict(orient="records")
    if not rows:
        pytest.skip("FPASS18 test data not found in CSV")
    row = rows[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # Extract email and password from CSV
    email = ""
    password = ""
    for line in test_data_str.splitlines():
        if line.strip().lower().startswith("email:"):
            email = line.split(":", 1)[1].strip()
        elif line.strip().lower().startswith("password:"):
            password = line.split(":", 1)[1].strip()

    fp_page = ForgotPasswordPage(page)

    try:
        # Navigate to Forgot Password → OTP → Set New Password
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()
        fp_page.enter_email(email)
        fp_page.click_next_button()  # OTP tab
        fp_page.click_next_button()   # Set New Password tab

        # Enter new password
        new_password_input = page.locator(ForgotPasswordPage.NEW_PASSWORD_INPUT)
        new_password_input.fill(password)

        # Check PASSWORD_EYE_ICON toggle using .first
        eye_icon_visible = page.locator(ForgotPasswordPage.PASSWORD_EYE_ICON).first.is_visible()
        if eye_icon_visible:
            fp_page.toggle_password_visibility()
            type_after_toggle = new_password_input.get_attribute("type")
            if type_after_toggle == "text":
                print("✅ Password visibility toggle works → Test Passed")
                update_csv_and_report(fp_page, request, "FPASS18", expected, True)
            else:
                print("❌ Password not revealed after toggle → Test Failed")
                update_csv_and_report(fp_page, request, "FPASS18", expected, False, "Toggle failed")
        else:
            print("❌ PASSWORD_EYE_ICON not visible → Test Failed")
            update_csv_and_report(fp_page, request, "FPASS18", expected, False, "Eye icon not visible")

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS18", expected, False, str(e))
        pytest.fail("FPASS18 failed")
def test_fpass19_confirm_password_input(page, request):
    # Get test data for FPASS19
    rows = test_data_df[test_data_df['TC ID'] == 'FPASS19'].to_dict(orient="records")
    if not rows:
        pytest.skip("FPASS19 test data not found in CSV")
    row = rows[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # Extract email, new password, confirm password
    email = ""
    new_password = ""
    confirm_password = ""
    for line in test_data_str.splitlines():
        if line.strip().lower().startswith("email:"):
            email = line.split(":", 1)[1].strip()
        elif line.strip().lower().startswith("password:"):
            new_password = line.split(":", 1)[1].strip()
        elif line.strip().lower().startswith("confirmpassword:"):
            confirm_password = line.split(":", 1)[1].strip()

    fp_page = ForgotPasswordPage(page)

    try:
        # Navigate to Set New Password tab
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()
        fp_page.enter_email(email)
        fp_page.click_next_button()   # OTP tab
        fp_page.click_next_button()   # Set New Password tab

        # Enter new password
        page.locator(ForgotPasswordPage.NEW_PASSWORD_INPUT).fill(new_password)

        # Enter confirm password
        fp_page.enter_confirm_password(confirm_password)

        # Validation
        entered_value = page.locator(ForgotPasswordPage.CONFIRM_PASSWORD_INPUT).input_value()
        if entered_value == confirm_password:
            print("✅ Confirm password entered → Test Passed")
            update_csv_and_report(fp_page, request, "FPASS19", expected, True)
        else:
            print("❌ Confirm password mismatch → Test Failed")
            update_csv_and_report(fp_page, request, "FPASS19", expected, False, "Confirm password not entered correctly")

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS19", expected, False, str(e))
        pytest.fail("FPASS19 failed")


def test_fpass20_password_mismatch(page, request):
    # Get test data for FPASS20
    rows = test_data_df[test_data_df['TC ID'] == 'FPASS20'].to_dict(orient="records")
    if not rows:
        pytest.skip("FPASS20 test data not found in CSV")
    row = rows[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # Extract email, password, confirm password
    email, password, confirm_password = "", "", ""
    for line in test_data_str.splitlines():
        if line.strip().lower().startswith("email:"):
            email = line.split(":", 1)[1].strip()
        elif line.strip().lower().startswith("password:"):
            password = line.split(":", 1)[1].strip()
        elif line.strip().lower().startswith("confirmpassword:"):
            confirm_password = line.split(":", 1)[1].strip()

    fp_page = ForgotPasswordPage(page)

    try:
        # Navigate to Set New Password tab
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()
        fp_page.enter_email(email)
        fp_page.click_next_button()   # OTP tab
        fp_page.click_next_button()   # Set New Password tab

        # Enter mismatch passwords using page class locators
        fp_page.enter_new_password(password)
        fp_page.enter_confirm_password(confirm_password)

        # Assert Register button disabled
        if not fp_page.is_register_button_enabled():
            print("✅ Password mismatch → Register button disabled → Test Passed")
            update_csv_and_report(fp_page, request, "FPASS20", expected, True)
        else:
            print("❌ Register button enabled with mismatch → Test Failed")
            update_csv_and_report(fp_page, request, "FPASS20", expected, False, "Mismatch allowed")
            pytest.fail("FPASS20 failed: Register button enabled with mismatched passwords")

    except Exception as e:
        print(f"❌ Exception occurred in FPASS20: {e}")
        update_csv_and_report(fp_page, request, "FPASS20", expected, False, str(e))
        pytest.fail(f"FPASS20 failed due to exception: {e}")

def test_fpass21_password_toggle(page, request):
    # Get test data for FPASS21
    rows = test_data_df[test_data_df['TC ID'] == 'FPASS21'].to_dict(orient="records")
    if not rows:
        pytest.skip("FPASS21 test data not found in CSV")
    row = rows[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # Extract email and password from CSV
    email = ""
    password = ""
    for line in test_data_str.splitlines():
        if line.strip().lower().startswith("email:"):
            email = line.split(":", 1)[1].strip()
        elif line.strip().lower().startswith("password:"):
            password = line.split(":", 1)[1].strip()

    fp_page = ForgotPasswordPage(page)

    try:
        # Step 1: Navigate to Set New Password tab
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()
        fp_page.enter_email(email)
        fp_page.click_next_button()   # OTP tab
        fp_page.click_next_button()   # Set New Password tab

        # Step 2: Enter new password and confirm password
        page.locator(ForgotPasswordPage.NEW_PASSWORD_INPUT).fill(password)
        page.locator(ForgotPasswordPage.CONFIRM_PASSWORD_INPUT).fill(password)

        # Step 3: Toggle New Password visibility
        page.locator(ForgotPasswordPage.NEW_PASSWORD_EYE_ICON).wait_for(state="visible", timeout=5000)
        page.locator(ForgotPasswordPage.NEW_PASSWORD_EYE_ICON).click(force=True)
        type_after_toggle_new = page.locator(ForgotPasswordPage.NEW_PASSWORD_INPUT).get_attribute("type")

        # Step 4: Toggle Confirm Password visibility
        page.locator(ForgotPasswordPage.CONFIRM_PASSWORD_EYE_ICON).wait_for(state="visible", timeout=5000)
        page.locator(ForgotPasswordPage.CONFIRM_PASSWORD_EYE_ICON).click(force=True)
        type_after_toggle_confirm = page.locator(ForgotPasswordPage.CONFIRM_PASSWORD_INPUT).get_attribute("type")

        # Step 5: Verify both fields toggled to text
        passed = (type_after_toggle_new == "text") and (type_after_toggle_confirm == "text")

        if passed:
            print("✅ Password toggle works for both fields → Test Passed")
            update_csv_and_report(fp_page, request, "FPASS21", expected, True)
        else:
            print("❌ Password toggle failed → Test Failed")
            update_csv_and_report(fp_page, request, "FPASS21", expected, False, "Toggle not working")     

    except Exception as e:
        # Save screenshot on failure
        page.screenshot(path=f"artifacts/reports/FPASS21_failure.png")
        update_csv_and_report(fp_page, request, "FPASS21", expected, False, str(e))
        pytest.fail(f"FPASS21 failed due to exception: {e}")

def test_fpass22_register_button_disabled_with_empty_passwords(page, request):
    # Get test data for FPASS22 (converted from FPASS37)
    rows = test_data_df[test_data_df['TC ID'] == 'FPASS22'].to_dict(orient="records")
    if not rows:
        pytest.skip("FPASS22 test data not found in CSV")
    row = rows[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # CSV like:
    # Email:admin@email.com
    # Password:""
    # confirmpassword:""
    email = ""
    password = ""
    confirm_password = ""

    for line in test_data_str.splitlines():
        key, sep, value = line.partition(":")
        if not sep:
            continue
        k = key.strip().lower()
        v = value.strip().strip('"').strip("'")  # handle "" in CSV
        if k == "email":
            email = v
        elif k == "password":
            password = v
        elif k == "confirmpassword":
            confirm_password = v

    fp_page = ForgotPasswordPage(page)

    try:
        # Navigate to Set New Password tab
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()
        fp_page.enter_email(email)
        fp_page.click_next_button()   # OTP tab
        fp_page.click_next_button()   # Set New Password tab

        # Ensure both password fields are empty
        page.locator(ForgotPasswordPage.NEW_PASSWORD_INPUT).fill("")        # explicit clear
        page.locator(ForgotPasswordPage.CONFIRM_PASSWORD_INPUT).fill("")    # explicit clear
        # If CSV provided empty strings, also apply them (no-op but keeps parity with your pattern)
        if password:
            page.locator(ForgotPasswordPage.NEW_PASSWORD_INPUT).fill(password)
        if confirm_password:
            page.locator(ForgotPasswordPage.CONFIRM_PASSWORD_INPUT).fill(confirm_password)

        # Assert Register button is disabled
        # Reuse your page object helper (used in FPASS20) and invert
        register_enabled = fp_page.is_register_button_enabled()
        passed = not register_enabled

        if passed:
            print("✅ Register button is disabled when passwords are empty → Test Passed")
            update_csv_and_report(fp_page, request, "FPASS22", expected, True)
        else:
            print("❌ Register button is enabled with empty passwords → Test Failed")
            update_csv_and_report(fp_page, request, "FPASS22", expected, False, "Register enabled with empty passwords")
            pytest.fail("FPASS22 failed: Register button enabled with empty passwords")

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS22", expected, False, str(e))
        pytest.fail(f"FPASS22 failed due to exception: {e}")

def test_fpass23_back_button(page, request):
    # Get test data for FPASS23
    rows = test_data_df[test_data_df['TC ID'] == 'FPASS23'].to_dict(orient="records")
    if not rows:
        pytest.skip("FPASS23 test data not found in CSV")
    row = rows[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    # Extract email from CSV
    email = ""
    for line in test_data_str.splitlines():
        if line.strip().lower().startswith("email:"):
            email = line.split(":", 1)[1].strip()

    fp_page = ForgotPasswordPage(page)

    try:
        # Step 1: Navigate to Forgot Password
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()
        fp_page.enter_email(email)

        # Step 2: Next → OTP tab → Next → Set New Password tab
        fp_page.click_next_button()   # OTP tab
        fp_page.click_next_button()   # Set New Password tab

        # Step 3: Click Back button
        page.locator(ForgotPasswordPage.BACK_BUTTON).click()

        # Step 4: Verify OTP tab active (4 input boxes visible)
        otp_inputs_count = page.locator(ForgotPasswordPage.OTP_INPUTS).count()
        passed = otp_inputs_count == 4

        if passed:
            print("✅ Back button navigated to OTP tab → Test Passed")
            update_csv_and_report(fp_page, request, "FPASS23", expected, True)
        else:
            print("❌ Back button did not return to OTP tab → Test Failed")
            update_csv_and_report(fp_page, request, "FPASS23", expected, False, "OTP tab not active")

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS23", expected, False, str(e))
        pytest.fail(f"FPASS23 failed due to exception: {e}")

def test_fpass24_modal_close_button(page, request):
    # Get test data for FPASS24
    rows = test_data_df[test_data_df['TC ID'] == 'FPASS24'].to_dict(orient="records")
    if not rows:
        pytest.skip("FPASS24 test data not found in CSV")
    row = rows[0]
    expected = row.get("Expected Result", "N/A")

    fp_page = ForgotPasswordPage(page)

    try:
        # Step 1: Navigate to Forgot Password modal
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()

        # Step 2: Verify X (Close) button is visible and enabled
        cross_btn = page.locator(ForgotPasswordPage.CROSS_BUTTON)
        expect(cross_btn).to_be_visible()
        expect(cross_btn).to_be_enabled()

        # Step 3: Click the button (no need to check modal state)
        page.wait_for_timeout(2000)
        cross_btn.click()

        print("✅ Cross button is present and clickable → Test Passed")
        update_csv_and_report(fp_page, request, "FPASS24", expected, True)

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS24", expected, False, str(e))
        pytest.fail(f"FPASS24 failed due to exception: {e}")

def test_fpass25_register_button(page, request):
    # Get test data for FPASS25
    rows = test_data_df[test_data_df['TC ID'] == 'FPASS25'].to_dict(orient="records")
    if not rows:
        pytest.skip("FPASS25 test data not found in CSV")
    row = rows[0]
    test_data_str = str(row.get("Test Data", ""))

    # Extract email and password from CSV
    email = ""
    password = ""
    for line in test_data_str.splitlines():
        if line.strip().lower().startswith("email:"):
            email = line.split(":", 1)[1].strip()
        elif line.strip().lower().startswith("password:"):
            password = line.split(":", 1)[1].strip()

    fp_page = ForgotPasswordPage(page)

    try:
        # Step 1: Navigate to Forgot Password → Set New Password
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()
        fp_page.enter_email(email)
        fp_page.click_next_button()  # OTP tab
        fp_page.click_next_button()  # Set New Password tab

        # Step 2: Enter new password and confirm password
        page.locator(ForgotPasswordPage.NEW_PASSWORD_INPUT).fill(password)
        page.locator(ForgotPasswordPage.CONFIRM_PASSWORD_INPUT).fill(password)

        # Step 3: Click Register button
        page.locator(ForgotPasswordPage.REGISTER_BUTTON).click()

        print("✅ Register button clicked successfully → Test Passed")
        update_csv_and_report(fp_page, request, "FPASS25", row.get("Expected Result", "N/A"), True)

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS25", row.get("Expected Result", "N/A"), False, str(e))
        pytest.fail(f"FPASS25 failed due to exception: {e}")

def test_fpass26_register_and_back_home(page, request):
    # Get test data for FPASS25
    rows = test_data_df[test_data_df['TC ID'] == 'FPASS26'].to_dict(orient="records")
    if not rows:
        pytest.skip("FPASS25 test data not found in CSV")
    row = rows[0]
    test_data_str = str(row.get("Test Data", ""))

    # Extract email and password from CSV
    email = ""
    password = ""
    for line in test_data_str.splitlines():
        if line.strip().lower().startswith("email:"):
            email = line.split(":", 1)[1].strip()
        elif line.strip().lower().startswith("password:"):
            password = line.split(":", 1)[1].strip()

    fp_page = ForgotPasswordPage(page)

    try:
        # Navigate to Set New Password tab
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()
        fp_page.enter_email(email)
        fp_page.click_next_button()  # OTP tab
        fp_page.click_next_button()  # Set New Password tab

        # Enter new password and confirm password
        page.locator(ForgotPasswordPage.NEW_PASSWORD_INPUT).fill(password)
        page.locator(ForgotPasswordPage.CONFIRM_PASSWORD_INPUT).fill(password)

        # Click Register button
        page.locator(ForgotPasswordPage.REGISTER_BUTTON).click()

        # Click Back to Home button
        page.locator(ForgotPasswordPage.BACK_TO_HOME_BUTTON).click()

        print("✅ Register and Back to Home clicked successfully → Test Passed")
        update_csv_and_report(fp_page, request, "FPASS26", row.get("Expected Result", "N/A"), True)

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS26", row.get("Expected Result", "N/A"), False, str(e))
        pytest.fail(f"FPASS25 failed due to exception: {e}")

def test_fpass27_escape_modal(page, request):
    # Get test data for FPASS27
    rows = test_data_df[test_data_df['TC ID'] == 'FPASS27'].to_dict(orient="records")
    if not rows:
        pytest.skip("FPASS27 test data not found in CSV")
    row = rows[0]

    fp_page = ForgotPasswordPage(page)

    try:
        # Step 1: Navigate to login and open Forgot Password modal
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()

        # Step 2: Press Escape key
        page.keyboard.press("Escape")
        time.sleep(2)

        # Step 3: Verify Forgot Password heading still visible
        heading_visible = fp_page.is_heading_visible()
        passed = heading_visible  # if True → modal is still open → passed

        if passed:
            print("✅ Modal remains open after pressing Escape → Test Passed")
            update_csv_and_report(fp_page, request, "FPASS27", row.get("Expected Result", "N/A"), True)
        else:
            print("❌ Modal closed after pressing Escape → Test Failed")
            update_csv_and_report(fp_page, request, "FPASS27", row.get("Expected Result", "N/A"), False, "Forgot Password heading not visible")

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS27", row.get("Expected Result", "N/A"), False, str(e))
        pytest.fail(f"FPASS27 failed due to exception: {e}")

def test_fpass28_backdrop_click(page, request):
    # Get test data for FPASS28
    rows = test_data_df[test_data_df['TC ID'] == 'FPASS28'].to_dict(orient="records")
    if not rows:
        pytest.skip("FPASS28 test data not found in CSV")
    row = rows[0]

    fp_page = ForgotPasswordPage(page)

    try:
        # Step 1: Navigate to login and open Forgot Password modal
        fp_page.navigate()
        fp_page.click_login_tab()
        fp_page.click_forgot_password_button()

        # Step 2: Click outside modal area (backdrop area)
        page.mouse.click(10, 10)  # clicking at top-left corner outside modal

        # Step 3: Small wait before verification
        page.wait_for_timeout(2000)

        # Step 4: Verify Forgot Password modal still visible
        heading_visible = fp_page.is_heading_visible()
        passed = heading_visible  # Modal should still be open

        if passed:
            print("✅ Modal remains open after backdrop click → Test Passed")
            update_csv_and_report(fp_page, request, "FPASS28", row.get("Expected Result", "N/A"), True)
        else:
            print("❌ Modal closed after backdrop click → Test Failed")
            update_csv_and_report(fp_page, request, "FPASS28", row.get("Expected Result", "N/A"), False, "Forgot Password modal closed unexpectedly")

    except Exception as e:
        update_csv_and_report(fp_page, request, "FPASS28", row.get("Expected Result", "N/A"), False, str(e))
        pytest.fail(f"FPASS28 failed due to exception: {e}")
