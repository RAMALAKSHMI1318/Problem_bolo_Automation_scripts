# import pytest
# import pandas as pd
# import os
# from pages.login_page import LoginPage
# from pages.country_page import CountryPage
# from pytest_html import extras

# EXCEL_FILE = "data/testdata.xlsx"
# TEMP_XLSX = "data/tempdata_temp.xlsx"

# # Read Excel once (country sheet)
# try:
#     test_data_df = pd.read_excel(EXCEL_FILE, sheet_name="country", engine="openpyxl")
# except Exception:
#     # Fallback without specifying engine (in case of environment differences)
#     test_data_df = pd.read_excel(EXCEL_FILE, sheet_name="country")

# # Ensure Status/Remarks are strings to avoid dtype warnings
# for col in ["Status", "Remarks"]:
#     if col in test_data_df.columns:
#         test_data_df[col] = test_data_df[col].astype(str)

# # -----------------------------
# # Drive tests purely by TC ID, in sheet order. Skip rows without TC ID.
# if "TC ID" in test_data_df.columns:
#     country_data_df = test_data_df[test_data_df["TC ID"].astype(str).str.strip() != ""]
# else:
#     country_data_df = test_data_df
# # -----------------------------

# # Convert filtered data to dict for parametrization
# test_data = country_data_df.to_dict(orient="records")


# @pytest.mark.parametrize("tc_index,tc", [(i, row) for i, row in enumerate(test_data)])
# def test_country_filters(page, tc_index, tc, request):
#     login_page = LoginPage(page)
#     country_page = CountryPage(page)

#     test_passed = False
#     error_msg = ""
#     expected_result = tc.get("Expected Result", "N/A")
#     tc_id = tc.get("TC ID", "").strip()

#     try:
#         # Login first
#         login_page.navigate("login")
#         login_page.login("admin@email.com", "password")

#         # Navigate to country page
#         country_page.open_country_page()

#         # Perform specific tab action based on TC ID
#         if tc_id == "COUNTRY02":
#             country_page.click_active_tab()
#         elif tc_id == "COUNTRY03":
#             country_page.click_inactive_tab()
#         elif tc_id == "COUNTRY04":
#             country_page.click_draft_tab()
#         elif tc_id == "COUNTRY05":
#             country_page.click_archive_tab()
#         elif tc_id == "COUNTRY07":
#             country_page.click_add_country_button()
#         elif tc_id == "COUNTRY08":
#             country_page.click_add_country_and_fill_form()
#         elif tc_id == "COUNTRY09":
#             country_page.hierarchy_and_fill_form("ProblemBolo_hierarchy.csv")
#         elif tc_id == "COUNTRY10":
#             country_page.jurisdiction_and_fill_form("ProblemBolo_jurisdiction.csv")
#         elif tc_id == "COUNTRY11": 
#             country_page.Geofence_and_fill_form()
#         elif tc_id == "COUNTRY12":
#             country_page.media_and_fill_form()
#         elif tc_id == "COUNTRY13":
#             country_page.summary_data()
#         elif tc_id in ["COUNTRY15", "COUNTRY16"]:
#             country_page.click_edit_modify_data(tc_id)
#         elif tc_id == "COUNTRY17":
#             country_page.click_onview()
#         else:
#             raise Exception(f"Unknown TC ID: {tc_id}")

#         # If no exception occurred, consider test passed
#         test_passed = True

#     except Exception as e:
#         error_msg = f"{tc_id} Exception: {str(e)}"
#         # Take screenshot
#         if not os.path.exists("reports"):
#             os.makedirs("reports")
#         screenshot_path = os.path.join("reports", f"{tc_id}_failure.png")
#         login_page.take_screenshot(screenshot_path)

#         if hasattr(request.config, "_html"):
#             request.config._html.extra.append(extras.image(screenshot_path))
#             request.config._html.extra.append(extras.text(error_msg))

#     finally:
#         # Update results in the in-memory DataFrame
#         last_index = country_data_df.index[tc_index]  # map to original dataframe index
#         if test_passed:
#             test_data_df.at[last_index, "Status"] = str("Passed")
#             test_data_df.at[last_index, "Remarks"] = str(expected_result)
#             if hasattr(request.config, "_html"):
#                 request.config._html.extra.append(extras.text(f"{tc_id} Passed"))
#         else:
#             test_data_df.at[last_index, "Status"] = str("Failed")
#             test_data_df.at[last_index, "Remarks"] = str(f"{expected_result} | Actual: {error_msg}")

#         # Always save to Excel output file as requested
#         test_data_df.to_excel(TEMP_XLSX, index=False)

#     # Fail the test if needed
#     if not test_passed:
#         pytest.fail(error_msg)




import pytest
import pandas as pd
import os
from pages.login_page import LoginPage
from pages.country_page import CountryPage
from pytest_html import extras

EXCEL_FILE = "data/testdata.xlsx"
TEMP_XLSX = "data/tempdata_temp.xlsx"

# Read Excel once (country sheet)
try:
    test_data_df = pd.read_excel(EXCEL_FILE, sheet_name="country", engine="openpyxl")
except Exception:
    # Fallback without specifying engine (in case of environment differences)
    test_data_df = pd.read_excel(EXCEL_FILE, sheet_name="country")

# Ensure Status/Remarks are strings to avoid dtype warnings
for col in ["Status", "Remarks"]:
    if col in test_data_df.columns:
        test_data_df[col] = test_data_df[col].astype(str)

# -----------------------------
# Drive tests purely by TC ID, in sheet order. Skip rows without TC ID.
if "TC ID" in test_data_df.columns:
    country_data_df = test_data_df[test_data_df["TC ID"].astype(str).str.strip() != ""]
else:
    country_data_df = test_data_df
# -----------------------------

# Convert filtered data to dict for parametrization
test_data = country_data_df.to_dict(orient="records")


@pytest.mark.parametrize("tc_index,tc", [(i, row) for i, row in enumerate(test_data)])
def test_country_filters(page, tc_index, tc, request):

    
    login_page = LoginPage(page)
    country_page = CountryPage(page)

    test_passed = False
    error_msg = ""
    expected_result = tc.get("Expected Result", "N/A")
    tc_id = tc.get("TC ID", "").strip()

    try:
        # Login first
        login_page.navigate("login")
        login_page.login("admin@email.com", "password")

        # Navigate to country page
        country_page.open_country_page()

        # Perform specific tab action based on TC ID
        if tc_id == "COUNTRY02":
            country_page.click_active_tab()
        elif tc_id == "COUNTRY03":
            country_page.click_inactive_tab()
        elif tc_id == "COUNTRY04":
            country_page.click_draft_tab()
        elif tc_id == "COUNTRY05":
            country_page.click_archive_tab()
        elif tc_id == "COUNTRY07":
            country_page.click_add_country_button()
        elif tc_id == "COUNTRY08":
            country_page.click_add_country_and_fill_form()
        elif tc_id == "COUNTRY09":
            country_page.hierarchy_and_fill_form("ProblemBolo_hierarchy.csv")
        elif tc_id == "COUNTRY10":
            country_page.jurisdiction_and_fill_form("ProblemBolo_jurisdiction.csv")
        elif tc_id == "COUNTRY11": 
            country_page.Geofence_and_fill_form()
        elif tc_id == "COUNTRY12":
            country_page.media_and_fill_form()
        elif tc_id == "COUNTRY13":
            country_page.summary_data()
        elif tc_id in ["COUNTRY15", "COUNTRY16"]:
            country_page.click_edit_modify_data(tc_id)
        elif tc_id == "COUNTRY17":
            country_page.click_onview()
        else:
            raise Exception(f"Unknown TC ID: {tc_id}")

        # If no exception occurred, consider test passed
        test_passed = True

    except Exception as e:
        error_msg = f"{tc_id} Exception: {str(e)}"
        # Take screenshot
        if not os.path.exists("reports"):
            os.makedirs("reports")
        screenshot_path = os.path.join("reports", f"{tc_id}_failure.png")
        login_page.take_screenshot(screenshot_path)

        if hasattr(request.config, "_html"):
            request.config._html.extra.append(extras.image(screenshot_path))
            request.config._html.extra.append(extras.text(error_msg))

    finally:
        # Update results in the in-memory DataFrame
        last_index = country_data_df.index[tc_index]  # map to original dataframe index
        if test_passed:
            test_data_df.at[last_index, "Status"] = str("Passed")
            test_data_df.at[last_index, "Remarks"] = str(expected_result)
            if hasattr(request.config, "_html"):
                request.config._html.extra.append(extras.text(f"{tc_id} Passed"))
        else:
            test_data_df.at[last_index, "Status"] = str("Failed")
            test_data_df.at[last_index, "Remarks"] = str(f"{expected_result} | Actual: {error_msg}")

        # Always save to Excel output file as requested
        test_data_df.to_excel(TEMP_XLSX, index=False)

    # Fail the test if needed
    if not test_passed:
        pytest.fail(error_msg)