import time
import pytest
import pandas as pd
import os
from pages.login_page import LoginPage
from pages.governance_page import GovernancePage
from config import CSV_FILE
from playwright.sync_api import Page
from pytest_html import extras

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
        page_obj.screenshot(path=screenshot_path)

        if hasattr(request.config, "_html"):
            request.config._html.extra.append(extras.image(screenshot_path))
            request.config._html.extra.append(extras.text(f"{tcid} Failed: {error}"))

    try:
        test_data_df.to_csv(CSV_FILE, index=False)
    except PermissionError:
        temp_csv = CSV_FILE.replace(".csv", "_temp.csv")
        test_data_df.to_csv(temp_csv, index=False)


def test_gov01_ministry_upload(page: Page, request):
    # ------------------ Load Test Data ------------------
    row = test_data_df[test_data_df['TC ID'] == 'GOV01'].to_dict(orient="records")[0]
    expected = row.get("Expected", "Ministry file uploaded successfully")
    test_data_str = row.get("Test Data", "")

    # ------------------ Parse Test Data ------------------
    data_map = {}
    for item in test_data_str.split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip()] = val.strip()

    # Extract variables
    email = data_map.get("email")
    password = data_map.get("password")
    country = data_map.get("country")
    state = data_map.get("state")
    district = data_map.get("district")
    city = data_map.get("city")
    ministry_file = data_map.get("MinistryFile")   # e.g. uploads/governanceV5/ministryV5.csv

    # ------------------ Page Objects ------------------
    login_page = LoginPage(page)
    governance_page = GovernancePage(page)

    try:
        # Step 1: Login
        login_page.navigate()
        login_page.login(email, password)

        # Step 2: Navigate Governance & Upload
        governance_page.navigate_to_governance()
        governance_page.select_location(country, state, district, city)
        governance_page.upload_btn.click()
        governance_page.upload_ministry_file(ministry_file)

        # Mark as passed
        update_csv_and_report(page, request, "GOV01", expected, True)

    except Exception as e:
        update_csv_and_report(page, request, "GOV01", expected, False, str(e))
        raise

def test_gov02_add_governance(page: Page, request):
    # ------------------ Load Test Data ------------------
    row = test_data_df[test_data_df['TC ID'] == 'GOV02'].to_dict(orient="records")[0]
    expected = row.get("Expected", "Governance roles created")
    data_map = {}
    for item in row["Test Data"].split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip()] = val.strip()

    email = data_map.get("email")
    password = data_map.get("password")
    country = data_map.get("country")
    state = data_map.get("state")
    district = data_map.get("district")
    city = data_map.get("city")
    ministry_file = data_map.get("MinistryFile")
    roles_file = data_map.get("RolesFile")

    # ------------------ Page Objects ------------------
    login_page = LoginPage(page)
    governance_page = GovernancePage(page)

    try:
        # Step 1: Login
        login_page.navigate()
        login_page.login(email, password)

        # Step 2: Navigate Governance
        governance_page.navigate_to_governance()
        governance_page.select_location(country, state, district, city)

        # Step 3: Upload Ministry file
        governance_page.upload_btn.click()
        governance_page.upload_ministry_file(ministry_file)


        # Step 4: Upload Roles file
        governance_page.upload_roles_file(roles_file)

        # Step 5: Optionally continue with further steps

        # ------------------ Update CSV/Report as Success ------------------
        update_csv_and_report(page, request, "GOV02", expected, True)

    except Exception as e:
        # ------------------ Update CSV/Report as Failure ------------------
        update_csv_and_report(page, request, "GOV02", expected, False, str(e))
        raise

def test_gov03_upload_governance(page: Page,request):
    # ------------------ Load Test Data ------------------
    test_data_df['TC ID'] = test_data_df['TC ID'].astype(str).str.strip()

    row = test_data_df[test_data_df['TC ID'] == 'GOV03'].to_dict(orient="records")[0]
    expected = row.get("Expected", "Governance roles created")
    data_map = {}
    for item in row["Test Data"].split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip()] = val.strip()

    email = data_map.get("email")
    password = data_map.get("password")
    country = data_map.get("country")
    state = data_map.get("state")
    district = data_map.get("district")
    city = data_map.get("city")
    ministry_file = data_map.get("MinistryFile")
    roles_file = data_map.get("RolesFile")
    officers_file = data_map.get("OfficersFile")  # Add to CSV if needed

    # ------------------ Page Objects ------------------
    login_page = LoginPage(page)
    governance_page = GovernancePage(page)

    try:
        # Step 1: Login
        login_page.navigate()
        login_page.login(email, password)

        # Step 2: Navigate Governance
        governance_page.navigate_to_governance()
        governance_page.select_location(country, state, district, city)
        governance_page.upload_btn.click()

        # Step 3: Upload Ministry file
        governance_page.upload_ministry_file(ministry_file)
        time.sleep(3)
        # Step 4: Upload Roles file
        governance_page.upload_roles_file(roles_file)
        time.sleep(3)

        # Step 5: Upload Officers file (if provided)
        if officers_file:
            governance_page.upload_officers_file(officers_file)

        update_csv_and_report(page, request, "GOV03", expected, True)
        

    except Exception as e:
        update_csv_and_report(page, request, "GOV03", expected, False, str(e))
        raise

def test_gov04_role_personnel_mapping(page: Page,request):
    row = test_data_df[test_data_df['TC ID'] == 'GOV04'].to_dict(orient="records")[0]
    expected = row.get("Expected", "Governance roles created")
    data_map = {}
    for item in row["Test Data"].split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip()] = val.strip()

    email = data_map.get("email")
    password = data_map.get("password")
    country = data_map.get("country")
    state = data_map.get("state")
    district = data_map.get("district")
    city = data_map.get("city")
    ministry_file = data_map.get("MinistryFile")
    roles_file = data_map.get("RolesFile")
    officers_file = data_map.get("OfficersFile")
    roles_assignments = data_map.get("RolesAssignments")

    login_page = LoginPage(page)
    governance_page = GovernancePage(page)

    try:
        login_page.navigate()
        login_page.login(email, password)

        governance_page.navigate_to_governance()
        governance_page.select_location(country, state, district, city)
        governance_page.upload_btn.click()
        governance_page.upload_ministry_file(ministry_file)
        time.sleep(3)
        governance_page.upload_roles_file(roles_file)
        time.sleep(3)
        governance_page.upload_officers_file(officers_file)

        governance_page.map_roles_to_personnel(roles_assignments)

        update_csv_and_report(page, request, "GOV04", expected, True)

    except Exception as e:
        update_csv_and_report(page, request, "GOV04", expected, False, str(e))
        raise

def test_gov05_edit_governance(page: Page, request):
    row = test_data_df[test_data_df['TC ID'] == 'GOV05'].to_dict(orient="records")[0]
    expected = row.get("Expected", "Governance body updated")

    data_map = {}
    for item in row["Test Data"].split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip()] = val.strip()

    email = data_map.get("email")
    password = data_map.get("password")
    country = data_map.get("country")
    state = data_map.get("state")
    district = data_map.get("district")
    city = data_map.get("city")
    updated_ministry_file = data_map.get("UpdatedMinistryFile")

    login_page = LoginPage(page)
    governance_page = GovernancePage(page)

    try:
        login_page.navigate()
        login_page.login(email, password)

        governance_page.navigate_to_governance()
        governance_page.select_location(country, state, district, city)

        governance_page.update_governance_body(updated_ministry_file)

        update_csv_and_report(page, request, "GOV05", expected, passed=True)

    except Exception as e:
        update_csv_and_report(page, request, "GOV05", expected, passed=False, error=str(e))
        raise

def test_gov06_update_roles(page: Page, request):
    # GOV06 row only
    row6 = test_data_df[test_data_df['TC ID'] == 'GOV06'].to_dict(orient="records")[0]
    expected6 = row6.get("Expected", "Governance roles updated")

    data_map6 = {}
    for item in row6["Test Data"].split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map6[key.strip()] = val.strip()

    email = data_map6.get("email")
    password = data_map6.get("password")
    country = data_map6.get("country")
    state = data_map6.get("state")
    district = data_map6.get("district")
    city = data_map6.get("city")
    updated_ministry_file = data_map6.get("UpdatedMinistryFile")
    updated_roles_file = data_map6.get("RolesFile")

    login_page = LoginPage(page)
    governance_page = GovernancePage(page)

    try:
        # Step 1: Login
        login_page.navigate()
        login_page.login(email, password)

        # Step 2: Navigate Governance
        governance_page.navigate_to_governance()
        governance_page.select_location(country, state, district, city)

        # Step 3: Update Ministry (process of GOV05 but no GOV05 CSV update)
        governance_page.update_governance_body(updated_ministry_file)

        # Step 4: Update Roles (GOV06)
        governance_page.update_roles_file(updated_roles_file)
        

        # ✅ Only GOV06 marked in CSV
        update_csv_and_report(page, request, "GOV06", expected6, passed=True)

    except Exception as e:
        update_csv_and_report(page, request, "GOV06", expected6, passed=False, error=str(e))
        raise

def test_gov07_view_governance(page: Page, request):
    # Fetch GOV07 row from CSV
    row = test_data_df[test_data_df['TC ID'] == 'GOV07'].to_dict(orient="records")[0]
    expected = row.get("Expected", "Complete governance structure displayed")

    data_map = {}
    for item in row["Test Data"].split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip()] = val.strip()

    email = data_map.get("email")
    password = data_map.get("password")
    country = data_map.get("country")
    state = data_map.get("state")
    district = data_map.get("district")
    city = data_map.get("city")

    # Initialize page objects
    login_page = LoginPage(page)
    governance_page = GovernancePage(page)

    try:
        # Step 1: Login
        login_page.navigate()
        login_page.login(email, password)

        # Step 2: Navigate to Governance page and select location
        governance_page.navigate_to_governance()
        governance_page.select_location(country, state, district, city)

        # Step 3: Perform view governance actions
        governance_page.view_governance()

        # Step 4: Update CSV as Passed
        update_csv_and_report(page, request, "GOV07", expected, passed=True)

    except Exception as e:
        # Step 5: Update CSV as Failed with screenshot
        update_csv_and_report(page, request, "GOV07", expected, passed=False, error=str(e))
        raise
