import random
import time
from playwright.sync_api import Page
import time
import pytest
import pandas as pd
import os
from pages.login_page import LoginPage
from pages.governance_page import GovernancePage
from config import CSV_FILE
from playwright.sync_api import Page
from pytest_html import extras

from pages.party_page import PartyPage
from utils.allure_helper import AllureHelper

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


def test_party01_add_party(page: Page, request):
   
    tcid="PARTY01"
    AllureHelper.attach_description(tcid)
    row = test_data_df[test_data_df['TC ID'] == 'PARTY01'].to_dict(orient="records")[0]
    expected = row.get("Expected", "Party created successfully")

    
    data_map = {}
    for item in row["Test Data"].split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip()] = val.strip()

    email = data_map.get("email")
    password = data_map.get("password")
    logo_file = data_map.get("partylogo", "uploads/partylogos/tdp.jpg")
    party_name = data_map.get("party_name")
    country = data_map.get("country")
    state = data_map.get("state")
    district = data_map.get("district")
    city = data_map.get("city")

  
    party_code = f"{random.randint(100, 999)}{int(time.time()) % 1000}"

    login_page = LoginPage(page)
    party_page = PartyPage(page)

    try:
        
        login_page.navigate()
        login_page.login(email, password)

       
        party_page.navigate_party_section()

        party_page.add_party(
            logo_file=logo_file,
            party_name=party_name,
            party_code=party_code,
            country=country,
            state=state,
            district=district,
            city=city
        )

      
        update_csv_and_report(page, request, "PARTY01", expected, passed=True)

    except Exception as e:
        update_csv_and_report(page, request, "PARTY01", expected, passed=False, error=str(e))
        raise

def test_party02_edit_party(page, request):

    tcid="PARTY02"
    AllureHelper.attach_description(tcid)
  
    row = test_data_df[test_data_df['TC ID'] == 'PARTY02'].to_dict(orient="records")[0]
    expected = row.get("Expected", "Party details updated")

    data_map = {}
    for item in row["Test Data"].split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip()] = val.strip()

    email = data_map.get("email")
    password = data_map.get("password")
    updated_name = data_map["party_name"]


    login_page = LoginPage(page)
    party_page = PartyPage(page)

    try:
       
        login_page.navigate()
        login_page.login(email, password)

       
        party_page.navigate_party_section()

       
        party_page.edit_party(search_text="telugu", updated_name=updated_name)

     
        update_csv_and_report(page, request, "PARTY02", expected, passed=True)

    except Exception as e:
        update_csv_and_report(page, request, "PARTY02", expected, passed=False, error=str(e))
        raise

def test_party03_view_party(page, request):

    tcid="PARTY03"
    AllureHelper.attach_description(tcid)
   
    row = test_data_df[test_data_df['TC ID'] == 'PARTY03'].to_dict(orient="records")[0]
    expected = row.get("Expected", "Complete party information displayed")

   
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

    login_page = LoginPage(page)
    party_page = PartyPage(page)

    try:
       
        login_page.navigate()
        login_page.login(email, password)

       
        party_page.navigate_party_sections(country, state, district, city)

        party_page.view_party()

        update_csv_and_report(page, request, "PARTY03", expected, passed=True)

    except Exception as e:
        update_csv_and_report(page, request, "PARTY03", expected, passed=False, error=str(e))
        raise
