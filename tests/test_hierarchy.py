import time
import pytest
import pandas as pd
import os
from pages.hierarchy_page import HierarchyPage
from pages.login_page import LoginPage
from pages.governance_page import GovernancePage
from config import CSV_FILE
from playwright.sync_api import Page
from pytest_html import extras

from pages.non_hierarchy_page import NonHierarchyPage
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

@pytest.mark.parametrize("tcid", ["HIER01"])
def test_hier01_hierarchy_pr(page, request, tcid):
    tcid="HIER01"
    AllureHelper.attach_description(tcid)
    row = test_data_df[test_data_df['TC ID'] == tcid].iloc[0]

    email = row["Test Data"].split("email:")[1].split(",")[0].strip()
    password = row["Test Data"].split("password:")[1].split(",")[0].strip()

   
    indexes_str = row["Test Data"].split("indexes:")[1].split(",")
    indexes = [int(i.strip()) for i in indexes_str]

    expected_result = row["Expected Result"]

    try:
      
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(email, password)

       
        hierarchy_page = HierarchyPage(page)
        hierarchy_page.create_hierarchy_pr(indexes)

       
        update_csv_and_report(page, request, tcid, expected_result, passed=True)

    except Exception as e:
        update_csv_and_report(page, request, tcid, expected_result, passed=False, error=str(e))
        pytest.fail(f"{tcid} failed due to {e}")

@pytest.mark.parametrize("tcid", ["HIER03"])
def test_hier03_upload_hierarchy(page, request, tcid):

    tcid="HIER03"
    AllureHelper.attach_description(tcid)
    row = test_data_df[test_data_df["TC ID"] == tcid].iloc[0]

    email = row["Test Data"].split("email:")[1].split(",")[0].strip()
    password = row["Test Data"].split("password:")[1].split(",")[0].strip()
    expected_result = row["Expected Result"]

   
    if "indexes:" in row["Test Data"]:
        indexes_str = row["Test Data"].split("indexes:")[1].strip(" []")
        indexes = [int(i.strip()) for i in indexes_str.split(",") if i.strip().isdigit()]
    else:
        indexes = []

    try:
    
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(email, password)

        hierarchy_page = HierarchyPage(page)
        hierarchy_page.create_jurisdiction_pr(indexes)

      
        update_csv_and_report(page, request, tcid, expected_result, passed=True)

    except Exception as e:
        update_csv_and_report(page, request, tcid, expected_result, passed=False, error=str(e))
        pytest.fail(f"{tcid} failed due to {e}")

@pytest.mark.parametrize("tcid", ["HIER04"])
def test_hier04_upload_hierarchy(page, request, tcid):
    tcid="HIER04"
    AllureHelper.attach_description(tcid)
    row = test_data_df[test_data_df["TC ID"] == tcid].iloc[0]

    email = row["Test Data"].split("email:")[1].split(",")[0].strip()
    password = row["Test Data"].split("password:")[1].split(",")[0].strip()
    expected_result = row["Expected Result"]

  
    if "indexes:" in row["Test Data"]:
        indexes_str = row["Test Data"].split("indexes:")[1].strip(" []")
        indexes = [int(i.strip()) for i in indexes_str.split(",") if i.strip().isdigit()]
    else:
        indexes = []

    try:
       
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(email, password)

        
        hierarchy_page = HierarchyPage(page)
        hierarchy_page.create_jurisdiction_pr(indexes)
        hierarchy_page.create_geofence()

        update_csv_and_report(page, request, tcid, expected_result, passed=True)

    except Exception as e:
        update_csv_and_report(page, request, tcid, expected_result, passed=False, error=str(e))
        pytest.fail(f"{tcid} failed due to {e}")

@pytest.mark.parametrize("tcid", ["HIER05"])
def test_hier05_upload_hierarchy(page, request, tcid):

    tcid="HIER05"
    AllureHelper.attach_description(tcid)
    row = test_data_df[test_data_df["TC ID"] == tcid].iloc[0]

    email = row["Test Data"].split("email:")[1].split(",")[0].strip()
    password = row["Test Data"].split("password:")[1].split(",")[0].strip()
    expected_result = row["Expected Result"]

    if "indexes:" in row["Test Data"]:
        indexes_str = row["Test Data"].split("indexes:")[1].strip(" []")
        indexes = [int(i.strip()) for i in indexes_str.split(",") if i.strip().isdigit()]
    else:
        indexes = []

    try:
      
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(email, password)

      
        hierarchy_page = HierarchyPage(page)
        hierarchy_page.create_jurisdiction_pr(indexes)
        hierarchy_page.create_geofence()
        hierarchy_page.create_roles()

    
        update_csv_and_report(page, request, tcid, expected_result, passed=True)

    except Exception as e:
        update_csv_and_report(page, request, tcid, expected_result, passed=False, error=str(e))
        pytest.fail(f"{tcid} failed due to {e}")

@pytest.mark.parametrize("tcid", ["HIER06"])
def test_hier06_upload_hierarchy(page, request, tcid):

    tcid="HIER06"
    AllureHelper.attach_description(tcid)
    row = test_data_df[test_data_df["TC ID"] == tcid].iloc[0]

    email = row["Test Data"].split("email:")[1].split(",")[0].strip()
    password = row["Test Data"].split("password:")[1].split(",")[0].strip()
    expected_result = row["Expected Result"]

   
    if "indexes:" in row["Test Data"]:
        indexes_str = row["Test Data"].split("indexes:")[1].strip(" []")
        indexes = [int(i.strip()) for i in indexes_str.split(",") if i.strip().isdigit()]
    else:
        indexes = []

    try:
        
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(email, password)

      
        hierarchy_page = HierarchyPage(page)
        hierarchy_page.create_jurisdiction_pr(indexes)
        hierarchy_page.create_geofence()
        hierarchy_page.create_roles()
        hierarchy_page.create_personnel()


      
        update_csv_and_report(page, request, tcid, expected_result, passed=True)

    except Exception as e:
        update_csv_and_report(page, request, tcid, expected_result, passed=False, error=str(e))
        pytest.fail(f"{tcid} failed due to {e}")

@pytest.mark.parametrize("tcid", ["HIER02"])
def test_hier02_hierarchy_full_flow(page, request, tcid):
    tcid="HIER02"
    AllureHelper.attach_description(tcid)
  
    row = test_data_df[test_data_df["TC ID"] == tcid].iloc[0]
    email = row["Test Data"].split("email:")[1].split(",")[0].strip()
    password = row["Test Data"].split("password:")[1].split(",")[0].strip()
    expected_result = row["Expected Result"]

  
    if "indexes:" in row["Test Data"]:
        indexes_str = row["Test Data"].split("indexes:")[1].strip(" []")
        indexes = [int(i.strip()) for i in indexes_str.split(",") if i.strip().isdigit()]
    else:
        indexes = []

    
    selections = {
        "jurisdiction": indexes[1:4], 
        "personal": indexes[4:7],      
        "party": indexes[7:10]      
    }

    try:
       
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(email, password)

     
        hierarchy_page = HierarchyPage(page)
        hierarchy_page.create_fullhierarchy_pr(indexes)

      
        hierarchy_page.fill_dropdowns_by_index(selections)

  
        print(f"✅ {tcid} executed successfully")
        update_csv_and_report(page, request, tcid, expected_result, passed=True)

    except Exception as e:
        error_message = str(e)
        print(f"\n❌ {tcid} failed due to: {error_message}")
        screenshot_path = os.path.join("artifacts", f"{tcid}_failure.png")
        page.screenshot(path=screenshot_path)
        if hasattr(request, "node"):
            request.node.user_properties.append(("screenshot", screenshot_path))
        update_csv_and_report(page, request, tcid, expected_result, passed=False, error=error_message)
        pytest.fail(f"{tcid} failed due to {error_message}")

@pytest.mark.parametrize("tcid", ["HIER07"])
def test_hier07_view_hierarchy(page, request, tcid):
    tcid="HIER07"
    AllureHelper.attach_description(tcid)
    row = test_data_df[test_data_df["TC ID"] == tcid].iloc[0]
    email = row["Test Data"].split("email:")[1].split(",")[0].strip()
    password = row["Test Data"].split("password:")[1].split(",")[0].strip()
    expected_result = row["Expected Result"]

    try:
        
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(email, password)

       
        hierarchy_page = HierarchyPage(page)
        hierarchy_page.view_hierarchy_summary("revanth")

    
        update_csv_and_report(page, request, tcid, expected_result, passed=True)
        print(f"✅ {tcid} executed successfully")

    except Exception as e:
        error_message = str(e)
        print(f"\n❌ {tcid} failed due to: {error_message}")
        screenshot_path = os.path.join("artifacts", f"{tcid}_failure.png")
        page.screenshot(path=screenshot_path)
        if hasattr(request, "node"):
            request.node.user_properties.append(("screenshot", screenshot_path))
        update_csv_and_report(page, request, tcid, expected_result, passed=False, error=error_message)
        pytest.fail(f"{tcid} failed due to {error_message}")

