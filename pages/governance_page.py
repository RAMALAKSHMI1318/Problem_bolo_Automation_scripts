import time
from playwright.sync_api import Page
import os

class GovernancePage:
    def __init__(self, page: Page):
        self.page = page

        # ---------- Locators ----------
        # Navigation
        self.get_started_btn = page.get_by_role("button", name="Get Started")
        self.governance_btn = page.get_by_role("button", name="Governance")

        # Location selectors (dropdowns)
        self.comboboxes = page.locator("div[role='combobox']:not([aria-labelledby='rows-per-page-label'])")

        # Upload common
        self.upload_btn = page.get_by_role("button", name="+ Upload Governance Data")
        self.download_btn = page.get_by_role("button", name="Download")
        self.file_input = page.locator("input#csv-upload")
        self.next_btn = page.get_by_role("button", name="Next")
# Example locators in governance_page.py
        self.dropdowns = page.locator(".MuiAutocomplete-root .MuiAutocomplete-popupIndicator")
        self.next_btn = page.get_by_role("button", name="Next")
        self.submit_btn = page.get_by_role("button", name="Submit")
        self.apply_btn = page.get_by_role("button", name="Apply")
        self.edit_icon_btn = page.get_by_role("button", name="primaryEditIcon").first
        self.view_icon_btn = self.page.get_by_role("button", name="primaryEyeIcon")
        self.close_btn = self.page.get_by_role("button", name="Close")
    # ---------- Functions ----------

    def navigate_to_governance(self):
        self.get_started_btn.click()
        self.governance_btn.click()
        self.page.wait_for_timeout(2000)

    def select_location(self, country, state, district, city):
        # Country
        self.comboboxes.nth(0).click()
        self.page.get_by_role("option", name=country).click()

        # State
        self.comboboxes.nth(1).click()
        self.page.get_by_role("option", name=state).click()

        # District
        self.comboboxes.nth(2).click()
        self.page.get_by_role("option", name=district).click()

        # City
        self.comboboxes.nth(3).click()
        self.page.get_by_role("option", name=city).click()

    def upload_file(self, relative_path: str):
        """Generic upload method (handles download + file upload)"""
        abs_path = os.path.abspath(relative_path)

        # Download sample
        with self.page.expect_download() as download_info:
            self.download_btn.click()
        download = download_info.value

        # Upload file
        self.file_input.set_input_files(abs_path)

        # Click Next
        self.next_btn.click()

    def upload_ministry_file(self, file_path: str):
        self.upload_file(file_path)

    def upload_roles_file(self, file_path: str):
        self.upload_file(file_path)

    def upload_officers_file(self, file_path: str):
        self.upload_file(file_path)

    def map_roles_to_personnel(self, roles_assignments: str):
        """
        roles_assignments format from CSV:
        Chief Minister|Rajendra Bhosale;
        Deputy Chief Minister|Swati Sameer Wadke;
        Municipal Minister|Anil Muley;
        Home Minister|Milind Sabnis
        """
        if not roles_assignments:
            return

        pairs = [x.strip() for x in roles_assignments.split(";") if "|" in x]

        for idx, pair in enumerate(pairs):
            role, person = pair.split("|", 1)
            print(f"Mapping {idx+1}: {role} → {person}")

            # Role dropdown = even index, Person dropdown = odd index
            role_dropdown = self.dropdowns.nth(idx * 2)
            person_dropdown = self.dropdowns.nth(idx * 2 + 1)

            # Select role
            role_dropdown.click()
            self.page.get_by_role("option", name=role, exact=True).click()

            # Select person
            person_dropdown.click()
            self.page.get_by_role("option", name=person, exact=True).click()

        # Save mappings
        self.next_btn.click()
        self.submit_btn.click()

    def update_governance_body(self, updated_ministry_file: str):
        """
        Update governance body by selecting edit and uploading new ministry file.
        """
        # After city is selected → click Apply
        self.apply_btn.click()

        # Click the edit icon to modify governance body
        self.edit_icon_btn.click()

        self.page.set_input_files("input[type='file']", updated_ministry_file)
        self.next_btn.click()

    def update_roles_file(self, roles_file: str):
        """Update governance roles with updated roles file."""
        
        self.page.set_input_files("input[type='file']", roles_file)

    # Wait for next section or Next button to appear again (if applicable)
        self.next_btn.wait_for(state="visible", timeout=10000)
        self.next_btn.click()

        self.next_btn.wait_for(state="visible", timeout=10000)
        self.next_btn.click()
        
        self.next_btn.wait_for(state="visible", timeout=10000)
        self.next_btn.click()

    # Wait for Submit button to be enabled
        self.submit_btn.wait_for(state="visible", timeout=30000)
        self.submit_btn.click()

    def view_governance(self):
        """Perform governance view actions: Apply → Eye Icon → Close."""
        self.apply_btn.click()
        self.view_icon_btn.first.click()
        self.close_btn.click()


        

