import allure
import pandas as pd
import os

# Load CSV once
csv_path = os.path.join(os.path.dirname(__file__), "../data/testdata.csv")
test_data_df = pd.read_csv(csv_path)

class AllureHelper:

    @staticmethod
    def attach_description(tcid: str):
        """
        Attach dynamic description for Allure report from CSV.
        """
        row = test_data_df[test_data_df["TC ID"] == tcid].to_dict(orient="records")
        if not row:
            return
        row = row[0]

        module = row.get("Module/Screen", "")
        title = row.get("Title", "")
        preconditions = row.get("Preconditions", "")
        steps = row.get("Test Steps", "")
        test_data = row.get("Test Data", "")
        expected = row.get("Expected Result", "")
        type_ = row.get("Type", "")
        priority = row.get("Priority", "")

        allure.dynamic.description_html(f"""
        <b>TC ID:</b> {tcid}<br>
        <b>Module/Screen:</b> {module}<br>
        <b>Title:</b> {title}<br>
        <b>Preconditions:</b> {preconditions}<br>
        <b>Test Steps:</b> {steps}<br>
        <b>Test Data:</b> {test_data}<br>
        <b>Expected Result:</b> {expected}<br>
        <b>Type:</b> {type_} | <b>Priority:</b> {priority}<br>
        """)
