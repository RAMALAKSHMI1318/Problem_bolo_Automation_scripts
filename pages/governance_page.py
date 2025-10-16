import time
from playwright.sync_api import Page
import os

class GovernancePage:
    def __init__(self, page: Page):
        self.page = page

        
        self.get_started_btn = page.get_by_role("button", name="Get Started")
        self.governance_btn = page.get_by_role("button", name="Governance")

       
        self.comboboxes = page.locator("div[role='combobox']:not([aria-labelledby='rows-per-page-label'])")

       
        self.upload_btn = page.get_by_role("button", name="+ Upload Governance Data")
        self.download_btn = page.get_by_role("button", name="Download")
        self.file_input = page.locator("input#csv-upload")
        self.next_btn = page.get_by_role("button", name="Next")

        self.dropdowns = page.locator("button.MuiAutocomplete-popupIndicator:visible")
        
        self.submit_btn = page.get_by_role("button", name="Submit")
        self.apply_btn = page.get_by_role("button", name="Apply")
        self.edit_icon_btn = page.get_by_role("button", name="primaryEditIcon").first
        self.view_icon_btn = self.page.get_by_role("button", name="primaryEyeIcon")
        self.close_btn = self.page.get_by_role("button", name="Close")
    

    def navigate_to_governance(self):
        self.get_started_btn.click()
        self.governance_btn.click()
        self.page.wait_for_timeout(2000)

    def select_location_by_index(self, indices: list):
        page = self.page
        comboboxes = self.comboboxes
        total = min(4, len(indices)) 

        print(f"Selecting location by index: {indices}")

        for i in range(total):
            try:
                index = indices[i]
                print(f"Selecting combobox {i} → option index {index}")

            
                comboboxes.nth(i).click()

            
                page.wait_for_selector('[role="option"]', state='visible', timeout=5000)

                page.get_by_role("option").nth(index).click()
                time.sleep(0.8)

            except Exception as e:
                print(f"⚠️ Failed to select combobox {i}: {e}")
                continue

        print("✅ Location selection by index completed.")

    def upload_file(self, relative_path: str):
        """Generic upload method (handles download + file upload)"""
        abs_path = os.path.abspath(relative_path)

        with self.page.expect_download() as download_info:
            self.download_btn.click()
        download = download_info.value

        self.file_input.set_input_files(abs_path)
        time.sleep(2)
 
        self.next_btn.click()

    def upload_ministry_file(self, file_path: str):
        self.upload_file(file_path)

    def upload_roles_file(self, file_path: str):
        self.upload_file(file_path)

    def upload_officers_file(self, file_path: str):
        self.upload_file(file_path)

    def fill_governance_dropdowns_by_index(self, selections: list):

        page = self.page
        dropdowns = page.locator(".MuiAutocomplete-popupIndicator")

        for i, index in enumerate(selections):
            print(f"Selecting dropdown {i} with option index {index}")
   
            dropdowns.nth(i).click()
        
       
            page.wait_for_selector('[role="option"]', state='visible', timeout=5000)
        
       
            page.get_by_role("option").nth(index).click()
            time.sleep(1)

    def update_governance_body(self, updated_ministry_file: str):
        """
        Update governance body by selecting edit and uploading new ministry file.
        """
        self.apply_btn.click()

        self.edit_icon_btn.click()
        time.sleep(2)

        self.page.set_input_files("input[type='file']", updated_ministry_file)
        self.next_btn.click()

    def update_roles_file(self, roles_file: str):
        """Update governance roles with updated roles file."""
        
        self.page.set_input_files("input[type='file']", roles_file)

        self.next_btn.wait_for(state="visible", timeout=10000)
        self.next_btn.click()

        self.next_btn.wait_for(state="visible", timeout=10000)
        self.next_btn.click()
        

    def view_governance(self):
        """Perform governance view actions: Apply → Eye Icon → Close."""
        self.apply_btn.click()
        self.view_icon_btn.first.click()
        self.close_btn.click()


        

