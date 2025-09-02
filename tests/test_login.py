import pytest
import pandas as pd
import re
import os
from pages.login_page import LoginPage
from pytest_html import extras

CSV_FILE = "data/testdata.csv"

# Read CSV once
test_data_df = pd.read_csv(CSV_FILE, engine="python")

# -----------------------------
# Filter rows up to TC ID = AUTH06
end_index = test_data_df[test_data_df['TC ID'].str.strip() == 'AUTH06'].index
if not end_index.empty:
    end_idx = end_index[0]
    # Slice the dataframe from top until AUTH06 (inclusive)
    test_data_df = test_data_df.loc[:end_idx]
else:
    test_data_df = pd.DataFrame()  # empty if AUTH06 not found
    print("TC ID AUTH06 not found in CSV, no tests will run.")
# -----------------------------

# Convert filtered data to dict for parametrization
test_data = test_data_df.to_dict(orient="records")


@pytest.mark.parametrize("tc_index,tc", [(i, row) for i, row in enumerate(test_data)])
def test_auth_and_registration(page, tc_index, tc, request):
    login_page = LoginPage(page)

    # Extract email/password from Test Data column using regex
    test_data_str = str(tc.get("Test Data", ""))
    email_match = re.search(r"Email:\s*([^\s]+)", test_data_str)
    password_match = re.search(r"Password:\s*([^\s]+)", test_data_str)

    email = email_match.group(1) if email_match else ""
    password = password_match.group(1) if password_match else ""

    test_passed = False
    error_msg = ""
    expected_result = tc.get("Expected Result", "N/A")

    try:
        # Navigate and perform login (up to Log-in button)
        login_page.navigate("login")
        login_page.login(email, password)

        # If no exception occurred, consider test passed
        test_passed = True

    except Exception as e:
        error_msg = f"{tc['TC ID']} Exception: {str(e)}"
        # Take screenshot
        if not os.path.exists("reports"):
            os.makedirs("reports")
        screenshot_path = os.path.join("reports", f"{tc['TC ID']}_failure.png")
        login_page.take_screenshot(screenshot_path)

        if hasattr(request.config, "_html"):
            request.config._html.extra.append(extras.image(screenshot_path))
            request.config._html.extra.append(extras.text(error_msg))

    finally:
        # Update CSV
        last_index = test_data_df.index[tc_index]  # map to original dataframe index
        if test_passed:
            test_data_df.at[last_index, "Status"] = "Passed"
            test_data_df.at[last_index, "Remarks"] = expected_result
            if hasattr(request.config, "_html"):
                request.config._html.extra.append(extras.text(f"{tc['TC ID']} Passed"))
        else:
            test_data_df.at[last_index, "Status"] = "Failed"
            test_data_df.at[last_index, "Remarks"] = f"{expected_result} | Actual: {error_msg}"

        # Save CSV safely
        try:
            test_data_df.to_csv(CSV_FILE, index=False)
        except PermissionError:
            temp_csv = CSV_FILE.replace(".csv", "_temp.csv")
            test_data_df.to_csv(temp_csv, index=False)

    # Fail the test if needed
    if not test_passed:
        pytest.fail(error_msg)
