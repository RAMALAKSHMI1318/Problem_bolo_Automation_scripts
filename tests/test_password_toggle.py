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

    
    email = ""
    if "Email:" in test_data_str:
        email = test_data_str.split("Email:")[1].strip()

    login_page = LoginPage(page)

    try:
        
        email_locator = page.get_by_text(email, exact=True)
        assert email_locator.is_visible(), f"Email {email} not visible on OTP tab"
        update_csv_and_report(login_page, request, "AUTH11", expected, True)
    except Exception as e:
        update_csv_and_report(login_page, request, "AUTH11", expected, False, str(e))
        pytest.fail("AUTH11 failed")
        
# ------------------ AUTH15 ------------------
def test_auth15_otp_input_ui(page, request):
    row = test_data_df[test_data_df['TC ID'] == 'AUTH15'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

   
    import re
    email_match = re.search(r"Email:\s*([^\s]+)", test_data_str, re.IGNORECASE)
    password_match = re.search(r"Password:\s*([^\s]+)", test_data_str, re.IGNORECASE)

    email = email_match.group(1).strip() if email_match else ""
    password = password_match.group(1).strip() if password_match else ""

    login_page = LoginPage(page)

    try:
       
        login_page.navigate()
        login_page.tab_login.click()

        
        login_page.input_email.fill(email)
        expect(login_page.input_password).to_be_visible(timeout=5000)
        login_page.input_password.fill(password)

        
        login_page.btn_next.click()

        # 
        expect(login_page.btn_next).to_be_enabled(timeout=10000)
        page.wait_for_timeout(1000)  
        login_page.btn_next.click()

        otp_inputs = page.locator("input[type='text'][maxlength='1']")
        expect(otp_inputs).to_have_count(4, timeout=5000)

        for i in range(4):
            expect(otp_inputs.nth(i)).to_be_visible()
            print(f"✅ OTP input {i+1} is visible")

        
        focused = page.evaluate(
            "document.activeElement === document.querySelector('input[type=text][maxlength=\"1\"]')"
        )

        update_csv_and_report(login_page, request, "AUTH15", expected, True)

    except Exception as e:
        update_csv_and_report(login_page, request, "AUTH15", expected, False, str(e))
        pytest.fail("AUTH15 failed")

# ------------------ AUTH16 ------------------
def test_auth16_otp_input_validation(page, request):
    row = test_data_df[test_data_df['TC ID'] == 'AUTH16'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    import re
    email_match = re.search(r"Email:\s*([^\s]+)", test_data_str, re.IGNORECASE)
    password_match = re.search(r"Password:\s*([^\s,]+)", test_data_str, re.IGNORECASE)
    otp_match = re.search(r"OTP:\s*([^\s]+)", test_data_str, re.IGNORECASE)

    email = email_match.group(1).strip() if email_match else ""
    password = password_match.group(1).strip() if password_match else ""
    otp_value = otp_match.group(1).strip() if otp_match else ""

    login_page = LoginPage(page)

    try:
        # -------------------- Step 1: Navigate & login --------------------
        login_page.navigate()
        login_page.tab_login.click()
        login_page.input_email.fill(email)
        expect(login_page.input_password).to_be_visible(timeout=5000)
        login_page.input_password.fill(password)

        login_page.btn_next.click()
        expect(login_page.btn_next).to_be_enabled(timeout=10000)
        page.wait_for_timeout(1000) 
        login_page.btn_next.click()

        
        otp_inputs = page.locator("input[type='text'][maxlength='1']")
        expect(otp_inputs).to_have_count(len(otp_value), timeout=5000)

        
        for i in range(len(otp_value)):
            otp_input = otp_inputs.nth(i)
            otp_input.fill("")
            otp_input.press("Backspace")
            otp_input.type(otp_value[i])

        
        all_valid = True
        for i, char in enumerate(otp_value):
            entered_char = otp_inputs.nth(i).input_value()
            if not char.isalnum() and entered_char != "":  
                all_valid = False
                print(f"❌ Invalid character '{entered_char}' was incorrectly accepted at OTP box {i+1}")
            else:
                print(f"✅ OTP box {i+1} is correct (entered '{entered_char}')")

       
        update_csv_and_report(login_page, request, "AUTH16", expected, all_valid)

        
        if not all_valid:
            pytest.fail("AUTH16 failed - special characters were accepted")

    except Exception as e:
        update_csv_and_report(login_page, request, "AUTH16", expected, False, str(e))
        pytest.fail("AUTH16 failed")

# ------------------ AUTH12 ------------------
def test_auth12_otp_auto_focus(page, request):
    row = test_data_df[test_data_df['TC ID'] == 'AUTH12'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    import re
    
    email_match = re.search(r"Email:\s*([^\s]+)", test_data_str, re.IGNORECASE)
    password_match = re.search(r"Password:\s*([^\s,]+)", test_data_str, re.IGNORECASE)
    otp_match = re.search(r"OTP:\s*([^\s]+)", test_data_str, re.IGNORECASE)

    email = email_match.group(1).strip() if email_match else ""
    password = password_match.group(1).strip() if password_match else ""
    otp_value = otp_match.group(1).strip() if otp_match else ""

    login_page = LoginPage(page)

    try:
        
        login_page.navigate()
        login_page.tab_login.click()
        login_page.input_email.fill(email)
        expect(login_page.input_password).to_be_visible(timeout=5000)
        login_page.input_password.fill(password)

        login_page.btn_next.click()
        expect(login_page.btn_next).to_be_enabled(timeout=10000)
        page.wait_for_timeout(1000)
        login_page.btn_next.click()

       
        otp_inputs = page.locator('input[type="text"][maxlength="1"]')
        expect(otp_inputs).to_have_count(len(otp_value), timeout=5000)

       
        for i in range(len(otp_value)):
            otp_inputs.nth(i).fill("")
            otp_inputs.nth(i).press("Backspace")

       
        auto_focus_passed = True
        for i, char in enumerate(otp_value):
            otp_inputs.nth(i).type(char)

            
            if i < len(otp_value) - 1:
                focused_index = page.evaluate(
                    'Array.from(document.querySelectorAll(\'input[type="text"][maxlength="1"]\')).indexOf(document.activeElement)'
                )
                if focused_index != i + 1:
                    auto_focus_passed = False
                    print(f"❌ Focus did NOT move to box {i+2} after typing in box {i+1}")
                else:
                    print(f"✅ Focus correctly moved to box {i+2}")

        if auto_focus_passed:
            print("✅ OTP auto-focus test PASSED")
        else:
            print("❌ OTP auto-focus test FAILED")

        # -------------------- Step 4: Update CSV/report --------------------
        update_csv_and_report(login_page, request, "AUTH12", expected, auto_focus_passed)

        if not auto_focus_passed:
            pytest.fail("AUTH12 failed - OTP auto-focus not working")

    except Exception as e:
        update_csv_and_report(login_page, request, "AUTH12", expected, False, str(e))
        pytest.fail("AUTH12 failed")

# -------------------- AUTH13: OTP Backspace Navigation --------------------
def test_auth13_otp_backspace(page, request):
    row = test_data_df[test_data_df['TC ID'] == 'AUTH13'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    import re
    # Extract Email, Password, OTP
    email_match = re.search(r"Email:\s*([^\s]+)", test_data_str, re.IGNORECASE)
    password_match = re.search(r"Password:\s*([^\s,]+)", test_data_str, re.IGNORECASE)
    otp_match = re.search(r"OTP:\s*([^\s]+)", test_data_str, re.IGNORECASE)

    email = email_match.group(1).strip() if email_match else ""
    password = password_match.group(1).strip() if password_match else ""
    otp_value = otp_match.group(1).strip() if otp_match else ""

    login_page = LoginPage(page)

    try:
        # -------------------- Step 1: Login --------------------
        login_page.navigate()
        login_page.tab_login.click()

        login_page.input_email.fill(email)
        expect(login_page.input_password).to_be_visible(timeout=5000)
        login_page.input_password.fill(password)

        login_page.btn_next.click()
        expect(login_page.btn_next).to_be_enabled(timeout=10000)
        page.wait_for_timeout(1000)
        login_page.btn_next.click()

        # -------------------- Step 2: OTP input --------------------
        otp_inputs = page.locator("input[type='text'][maxlength='1']")
        expect(otp_inputs).to_have_count(len(otp_value), timeout=5000)

        # Step 3: Clear auto-generated OTP
        for i in range(len(otp_value)):
            otp_inputs.nth(i).fill("")
            otp_inputs.nth(i).press("Backspace")

        # Step 4: Enter OTP from CSV
        for i, char in enumerate(otp_value):
            otp_inputs.nth(i).type(char)
            page.wait_for_timeout(50)  # tiny delay for UI to register

        # Step 5: Backspace Navigation
        backspace_worked = True
        for i in range(len(otp_value)-1, 0, -1):  # Start from last OTP box
            otp_input = otp_inputs.nth(i)
            otp_input.fill("")            
            page.wait_for_timeout(50)     
            otp_input.press("Backspace")  
            otp_input.press("Backspace") 

           
            active_index = page.evaluate("""
                () => Array.from(document.querySelectorAll('input[type="text"][maxlength="1"]'))
                      .indexOf(document.activeElement)
            """)
            if active_index != i - 1:
                backspace_worked = False
                print(f"❌ Backspace on OTP box {i+1} did NOT move focus to box {i}")
            else:
                print(f"✅ Focus correctly moved to OTP box {i}")

       
        update_csv_and_report(login_page, request, "AUTH13", expected, backspace_worked)

        if not backspace_worked:
            pytest.fail("AUTH13 failed: Backspace navigation did not work correctly")

    except Exception as e:
        update_csv_and_report(login_page, request, "AUTH13", expected, False, str(e))
        pytest.fail("AUTH13 failed")

def test_auth14_resend_otp_timer(page, request):
   
    rows = test_data_df[test_data_df['TC ID'] == 'AUTH14'].to_dict(orient="records")
    if not rows:
        pytest.skip("AUTH14 test data not found in CSV")
    row = rows[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    
    email, password = "", ""
    for line in test_data_str.splitlines():
        if line.strip().lower().startswith("email:"):
            email = line.split(":", 1)[1].strip()
        elif line.strip().lower().startswith("password:"):
            password = line.split(":", 1)[1].strip()

    login_page = LoginPage(page)

    try:
        
        login_page.navigate()
        login_page.tab_login.click()
        login_page.input_email.fill(email)
        login_page.input_password.fill(password)
        login_page.btn_next.click()
        page.wait_for_timeout(1000)
        login_page.btn_next.click() 

       
        print("⏳ Waiting 20 seconds for countdown...")
        page.wait_for_timeout(20000)

       
        expect(login_page.resend_button).to_be_visible(timeout=5000)
        expect(login_page.resend_button).to_be_enabled()
        print("✅ Resend button is visible and enabled after 20 seconds")

        update_csv_and_report(login_page, request, "AUTH14", expected, True)

    except Exception as e:
        update_csv_and_report(login_page, request, "AUTH14", expected, False, str(e))
        pytest.fail("AUTH14 failed")

def test_auth17_keyboard_navigation(page, request):
    
    rows = test_data_df[test_data_df['TC ID'] == 'AUTH17'].to_dict(orient="records")
    if not rows:
        pytest.skip("AUTH17 test data not found in CSV")
    row = rows[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    
    email, password = "", ""
    for line in test_data_str.splitlines():
        if line.strip().lower().startswith("email:"):
            email = line.split(":", 1)[1].strip()
        elif line.strip().lower().startswith("password:"):
            password = line.split(":", 1)[1].strip()

    login_page = LoginPage(page)

    try:
        
        login_page.navigate()
        login_page.tab_login.click()

       
        login_page.input_email.fill(email)
        login_page.input_password.fill(password)

       
        login_page.input_password.press("Enter")

        
        expect(login_page.masked_email).to_be_visible(timeout=5000)
        email_text = login_page.masked_email.inner_text()
        print(f"✅ Masked email text is visible: {email_text}")

        
        update_csv_and_report(login_page, request, "AUTH17", expected, True)

    except Exception as e:
        update_csv_and_report(login_page, request, "AUTH17", expected, False, str(e))
        pytest.fail("AUTH17 failed")


def test_auth18_logout_functionality(page, request):
    rows = test_data_df[test_data_df['TC ID'] == 'AUTH18'].to_dict(orient="records")
    if not rows:
        pytest.skip("AUTH18 test data not found in CSV")
    row = rows[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = str(row.get("Test Data", ""))

    email, password = "", ""
    for line in test_data_str.splitlines():
        if line.strip().lower().startswith("email:"):
            email = line.split(":", 1)[1].strip()
        elif line.strip().lower().startswith("password:"):
            password = line.split(":", 1)[1].strip()

    login_page = LoginPage(page)

    try:
       
        login_page.navigate()
        login_page.login(email, password)

       
        login_page.btn_get_started.click()
        login_page.btn_admin_menu.click()
        login_page.tab_settings.click()
        login_page.tab_account_settings.wait_for(state="visible", timeout=10000)
        login_page.tab_account_settings.click()
        login_page.btn_logout.wait_for(state="visible", timeout=10000)
        login_page.btn_logout.click()

        update_csv_and_report(login_page, request, "AUTH18", expected, True)
        print("✅ AUTH18: Logout clicked (no verification)")

    except Exception as e:
        update_csv_and_report(login_page, request, "AUTH18", expected, False, str(e))
        pytest.fail("AUTH18 failed")
