import random
import pytest
import pandas as pd
import os
import time
from pages.login_page import LoginPage
from pages.personnel_page import PersonnelPage
from config import CSV_FILE
from pytest_html import extras
from playwright.sync_api import Page

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


def test_pers02_add_personnel(page: Page, request):
    # ------------------ Load Test Data ------------------
    row = test_data_df[test_data_df['TC ID'] == 'PERS02'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = row.get("Test Data", "")

    # ------------------ Parse Test Data safely ------------------
    data_map = {}
    for item in test_data_str.split(","):
        if ":" in item:
            key, val = item.split(":", 1)  
            data_map[key.strip()] = val.strip()

    
    email = data_map.get("Email")
    password = data_map.get("password")
    firstname = data_map.get("firstname")
    lastname = data_map.get("lastname")
    address = data_map.get("address")

    
    timestamp = int(time.time())
    personal_email = f"{firstname.lower()}{timestamp}@example.com"
    personal_email_id = f"{lastname.lower()}{timestamp}"
    dynamic_phone = f"+91{random.randint(1000000000, 9999999999)}"

    
    login_page = LoginPage(page)
    personnel_page = PersonnelPage(page)

    try:
        
        login_page.navigate()      
        login_page.login(email, password)  

        
        personnel_page.add_personnel(
            firstname=firstname,
            lastname=lastname,
            phone=dynamic_phone,
            email=personal_email,
            empid=personal_email_id,
            address=address
        )

        
        update_csv_and_report(personnel_page, request, "PERS02", expected, True)
        print("✅ PERS02: Personnel workflow completed (Done clicked only)")

    except Exception as e:
       
        update_csv_and_report(personnel_page, request, "PERS02", expected, False, str(e))
        pytest.fail(f"PERS02 failed: {str(e)}")

def test_pers03_select_profile(page: Page, request):
    
    row = test_data_df[test_data_df['TC ID'] == 'PERS03'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = row.get("Test Data", "")

    
    data_map = {}
    for item in test_data_str.split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip()] = val.strip()

    
    email = data_map.get("Email")
    password = data_map.get("password")
    org_type = data_map.get("profileType", "Governance")  # Governance/Administrator

    
    login_page = LoginPage(page)
    personnel_page = PersonnelPage(page)

    try:
       
        login_page.navigate()
        login_page.login(email, password)

        
        personnel_page.btn_get_started.click()
        personnel_page.btn_personnel.click()
        personnel_page.btn_add_personnel.click()

      
        personnel_page.select_org_types(org_type)

        
        update_csv_and_report(personnel_page, request, "PERS03", expected, True)
        print(f"✅ PERS03: Organization type '{org_type}' selected successfully")

    except Exception as e:
    
        update_csv_and_report(personnel_page, request, "PERS03", expected, False, str(e))
        pytest.fail(f"PERS03 failed: {str(e)}")

def test_pers04_assign_jurisdiction(page: Page, request):
    # ------------------ Load Test Data ------------------
    row = test_data_df[test_data_df['TC ID'] == 'PERS04'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = row.get("Test Data", "")

   
    data_map = {}
    for item in test_data_str.split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip()] = val.strip()

   
    email = data_map.get("Email")
    password = data_map.get("password")
    org_type = data_map.get("profileType", "Governance")  

   
    login_page = LoginPage(page)
    personnel_page = PersonnelPage(page)

    try:
       
        login_page.navigate()
        login_page.login(email, password)

       
        personnel_page.navigate_and_select_location(org_type=org_type)

        # Step 3: (Optional) Select jurisdiction if needed
        # Example: personnel_page.cmb_jurisdiction.click()
        #          personnel_page.page.get_by_role("option", name="TestJurisdiction").click()

        
        update_csv_and_report(personnel_page, request, "PERS04", expected, True)
        print(f"✅ PERS04: Personnel location workflow completed for {email}")

    except Exception as e:
       
        update_csv_and_report(personnel_page, request, "PERS04", expected, False, str(e))
        pytest.fail(f"PERS04 failed for {email}: {str(e)}")

def test_pers05_institution_assignment(page: Page, request):
    # ------------------ Load Test Data ------------------
    row = test_data_df[test_data_df['TC ID'] == 'PERS05'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = row.get("Test Data", "")

    
    data_map = {}
    for item in test_data_str.split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip()] = val.strip()

   
    email = data_map.get("Email")
    password = data_map.get("password")
    institution = data_map.get("institution")  

   
    login_page = LoginPage(page)
    personnel_page = PersonnelPage(page)

    try:
        
        login_page.navigate()
        login_page.login(email, password)

       
        personnel_page.assign_institution_admin(institution_name=institution)

       
        update_csv_and_report(personnel_page, request, "PERS05", expected, True)
        print(f"✅ PERS05: Institution '{institution}' assigned successfully for {email}")

    except Exception as e:
        
        update_csv_and_report(personnel_page, request, "PERS05", expected, False, str(e))
        pytest.fail(f"PERS05 failed for {email}: {str(e)}")


def test_pers06_edit_personnel(page: Page, request):
    # ------------------ Load Test Data ------------------
    row = test_data_df[test_data_df['TC ID'] == 'PERS06'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = row.get("Test Data", "")

    
    data_map = {}
    for item in test_data_str.split(","):
        if ":" in item or "=" in item:
            key, val = item.replace("=", ":").split(":", 1)  # normalize separator
            data_map[key.strip()] = val.strip()

    
    email = data_map.get("Email")
    password = data_map.get("password")
    search_name = data_map.get("search_name")
    updated_last_name = data_map.get("name", "Updated Name")

    
    login_page = LoginPage(page)
    personnel_page = PersonnelPage(page)

    try:
        
        login_page.navigate()
        login_page.login(email, password)

       
        personnel_page.edit_personnel(search_name, updated_last_name)

        
        update_csv_and_report(personnel_page, request, "PERS06", expected, True)
        print(f"✅ PERS06: Personnel '{search_name}' updated to '{updated_last_name}'")

    except Exception as e:
        
        update_csv_and_report(personnel_page, request, "PERS06", expected, False, str(e))
        pytest.fail(f"PERS06 failed for {search_name}: {str(e)}")

def test_pers07_view_personnel(page: Page, request):
    # ------------------ Load Test Data ------------------
    row = test_data_df[test_data_df['TC ID'] == 'PERS07'].to_dict(orient="records")[0]
    expected = row.get("Expected Result", "N/A")
    test_data_str = row.get("Test Data", "")

    
    data_map = {}
    for item in test_data_str.split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip()] = val.strip()

    
    email = data_map.get("Email")
    password = data_map.get("password")
    search_name = data_map.get("search_name")

    
    login_page = LoginPage(page)
    personnel_page = PersonnelPage(page)

    try:
       
        login_page.navigate()
        login_page.login(email, password)

       
        personnel_page.view_personnel(search_name)

       
        update_csv_and_report(personnel_page, request, "PERS07", expected, True)
        print(f"✅ PERS07: Viewed personnel '{search_name}' successfully")

    except Exception as e:
       
        update_csv_and_report(personnel_page, request, "PERS07", expected, False, str(e))
        pytest.fail(f"PERS07 failed for {search_name}: {str(e)}")
