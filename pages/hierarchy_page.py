import os
import time
from playwright.sync_api import Page

class HierarchyPage:
    def __init__(self, page: Page):
        self.page = page
        self.btn_get_started = page.get_by_role("button", name="Get Started")
        self.btn_hierarchy_pr = page.get_by_role("button", name="Hierarchy PR").nth(1)
        self.btn_apply = page.get_by_role("button", name="Apply")
        self.btn_upload_hierarchy = page.get_by_role("button", name="+ Upload Hierarchy Data")
        self.btn_next = page.get_by_role("button", name="Next")
        self.dropdowns = page.get_by_role("combobox")
        self.input_file = page.locator("input[type='file']")

        self.dropdown_autocomplete_icon = page.locator(
            ".MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.MuiAutocomplete-popupIndicator"
        ).first

        self.dropdown_jurisdiction_0 = page.get_by_role("combobox", name="Select Jurisdiction").nth(0)
        self.dropdown_jurisdiction_1 = page.get_by_role("combobox", name="Select Jurisdiction").nth(1)
        self.dropdown_jurisdiction_2 = page.get_by_role("combobox", name="Select Jurisdiction").nth(2)

        self.dropdown_personal_0 = page.get_by_role("combobox", name="Select Personal").nth(0)
        self.dropdown_personal_1 = page.get_by_role("combobox", name="Select Personal").nth(1)
        self.dropdown_personal_2 = page.get_by_role("combobox", name="Select Personal").nth(2)

        self.dropdown_party_0 = page.get_by_role("combobox", name="Select Party").nth(0)
        self.dropdown_party_1 = page.get_by_role("combobox", name="Select Party").nth(1)
        self.dropdown_party_2 = page.get_by_role("combobox", name="Select Party").nth(2)

        self.dropdown_generic_endAdornment_0 = page.locator(
            "div:nth-child(4) > .MuiFormControl-root > .MuiInputBase-root > .MuiAutocomplete-endAdornment > .MuiButtonBase-root"
        ).first
        self.dropdown_generic_endAdornment_1 = page.locator(
            "div:nth-child(4) > .MuiBox-root > div > .MuiFormControl-root > .MuiInputBase-root > .MuiAutocomplete-endAdornment > .MuiButtonBase-root"
        ).first

        self.btn_submit = page.get_by_role("button", name="Submit")

        self.search_box = page.get_by_role("textbox", name="Search")
        
        self.first_eye_icon = page.get_by_role("button", name="primaryEyeIcon").first
        self.btn_close = page.get_by_role("button", name="Close")

    def select_dropdowns_by_index(self, indexes: list):
        """Select dropdowns dynamically based on index values."""
        for i, index in enumerate(indexes):
            dropdown = self.page.get_by_role("combobox").nth(i)
            dropdown.click()
            options = self.page.get_by_role("option")
            options.nth(index).click()
            self.page.wait_for_timeout(1000)  
    
    def create_hierarchy_pr(self, indexes: list):
        """Complete the Non-hierarchy PR setup."""
        self.btn_get_started.click()
        self.page.wait_for_timeout(2000)

        self.btn_hierarchy_pr.click()
        self.page.wait_for_timeout(2000)

        self.select_dropdowns_by_index(indexes)
        self.btn_apply.click()
        self.page.wait_for_timeout(2000)

    def create_jurisdiction_pr(self, indexes):
    
        self.btn_get_started.click()
        self.page.wait_for_timeout(1000)
        self.btn_hierarchy_pr.click()
        self.page.wait_for_timeout(1000)

  
        if len(indexes) > 0:
            self.dropdowns.nth(0).click()
            self.page.get_by_role("option").nth(indexes[0]).click()
            self.page.wait_for_timeout(500)

   
        self.btn_upload_hierarchy.wait_for(state="visible") 
        self.btn_upload_hierarchy.click()
        self.page.wait_for_timeout(500)

    
        if len(indexes) > 1:
            self.dropdowns.nth(0).click()
            self.page.get_by_role("option").nth(indexes[1]).click()
            self.page.wait_for_timeout(500)

        self.btn_next.click()
        self.page.wait_for_timeout(2000)
    
        upload_file_path = os.path.join("uploads", "hierarchy", "ProblemBolo_jurisdiction.csv")
        self.input_file.set_input_files(upload_file_path)
        self.page.wait_for_timeout(2000)

        self.btn_next.click()
        self.page.wait_for_timeout(1500)

    def create_geofence(self):
        upload_file_path1 = os.path.join("uploads", "hierarchy", "Hyderabad.kml")

       
        self.input_file.set_input_files(upload_file_path1)
        self.page.wait_for_timeout(1500)
        self.btn_next.click()
        self.page.wait_for_timeout(1500)
    
    def create_roles(self):
        upload_file_path1 = os.path.join("uploads", "hierarchy", "ProblemBolo_roles.csv")

     
        self.input_file.set_input_files(upload_file_path1)
        self.page.wait_for_timeout(1500)
        self.btn_next.click()
        self.page.wait_for_timeout(1500)

    def create_personnel(self):
        upload_file_path1 = os.path.join("uploads", "hierarchy", "ProblemBolo_personnel.csv")

        
        self.input_file.set_input_files(upload_file_path1)
        self.page.wait_for_timeout(1500)
        self.btn_next.click()
        self.page.wait_for_timeout(1500)

    def create_personnel2(self):
        upload_file_path1 = os.path.join("uploads", "hierarchy", "ProblemBolo_personnel2.csv")

        self.input_file.set_input_files(upload_file_path1)
        self.page.wait_for_timeout(1500)
        self.btn_next.click()
        self.page.wait_for_timeout(1500)

    def create_fullhierarchy_pr(self,indexes):
        self.create_jurisdiction_pr(indexes)
        self.create_geofence()
        self.create_roles()
        self.create_personnel2()

    def fill_dropdowns_by_index(self, selections):
        page = self.page

        for i in range(3):
    
            dropdown_jurisdiction = getattr(self, f"dropdown_jurisdiction_{i}")
            dropdown_jurisdiction.click()
            page.wait_for_selector('[role="option"]', state='visible', timeout=5000)
            page.get_by_role("option").nth(selections["jurisdiction"][i]).click()

        
            dropdown_personal = getattr(self, f"dropdown_personal_{i}")
            dropdown_personal.click()
            page.wait_for_selector('[role="option"]', state='visible', timeout=5000)
            page.get_by_role("option").nth(selections["personal"][i]).click()

       
            dropdown_party = getattr(self, f"dropdown_party_{i}")
            dropdown_party.click()
            page.wait_for_selector('[role="option"]', state='visible', timeout=5000)
            page.get_by_role("option").nth(selections["party"][i]).click()

   
        self.btn_next.click()
        self.btn_submit.click()

    def view_hierarchy_summary(self, representative_name: str):

        self.btn_get_started.click()

        self.btn_hierarchy_pr.click()

        self.search_box.click()
        self.search_box.fill(representative_name)

        self.first_eye_icon.click()
        time.sleep(2)

        self.btn_close.click()
        

