import time
from playwright.sync_api import Page
from base.base_page import BasePage


class PersonnelPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- Dashboard / navigation ---
        self.btn_get_started = page.get_by_role("button", name="Get Started")
        self.btn_personnel = page.get_by_role("button", name="Personnel")
        self.btn_add_personnel = page.get_by_role("button", name="+ Add Personnel")

        # --- Step 1: Organization type ---
        self.dropdown_org_type = page.get_by_label("", exact=True)
        self.option_governance = page.get_by_role("option", name="Governance")
        self.option_administrator = page.get_by_role("option", name="Administrator")


        # --- Step 2: Location selectors ---
        self.cmb_country = page.get_by_role("combobox").nth(0)
        self.option_india = page.get_by_role("option", name="India")

        self.cmb_state = page.get_by_role("combobox").nth(1)
        self.option_telangana = page.get_by_role("option", name="Telangana")

        self.cmb_city = page.get_by_role("combobox").nth(2)
        self.option_hyderabad = page.get_by_role("option", name="Hyderabad")

        self.cmb_area = page.get_by_role("combobox").nth(3)
        self.option_hydcity = page.get_by_role("option", name="HyderabadCity")

        # --- Step 3: Personnel details ---
        self.input_first_name = page.get_by_placeholder("Enter First Name")
        self.input_last_name = page.get_by_placeholder("Enter Last Name")
        self.input_phone = page.locator("input[type='tel']")
        self.input_email = page.get_by_role("textbox", name="Enter Email")
        self.input_empid = page.get_by_role("textbox", name="Enter Emp-id")
        self.input_address = page.get_by_role("textbox", name="Enter Address")

        # --- Navigation buttons ---
        self.btn_next = page.get_by_role("button", name="Next")
        self.btn_done = page.get_by_role("button", name="Done")
        self.profile_admin = page.get_by_text("ProfileAdministrator")
        self.cmb_institution = page.get_by_role("combobox")

        self.input_search_personnel = page.get_by_role("textbox", name="Search Personnel")
        self.btn_edit_personnel_icon = page.get_by_role("button", name="primaryEditIcon")
        self.txt_edit_personnel_header = page.get_by_text("Edit PersonnelAuto Saved To")
        self.input_last_name_edit = page.get_by_role("textbox").nth(1)   # based on your steps
        self.btn_edit_personnel_submit = page.get_by_role("button", name="Edit Personnel")
        self.btn_view_personnel = page.get_by_role("button", name="primaryEyeIcon")
        self.btn_close_view = page.get_by_role("button", name="Close")

    # ---------------- ACTION METHODS ----------------
    def navigate_to_personnel(self):
        self.btn_get_started.click()
        self.btn_personnel.click()
        self.btn_add_personnel.click()

    def select_org_type(self):
        self.dropdown_org_type.click()
        self.option_governance.click()
        self.btn_next.click()

    def select_location(self):
        self.cmb_country.click()
        self.option_india.click()
        self.cmb_state.click()
        self.option_telangana.click()
        self.cmb_city.click()
        self.option_hyderabad.click()
        self.cmb_area.click()
        self.option_hydcity.click()
        self.btn_next.click()

    def fill_personnel_details(self, first_name, last_name, phone, email, empid, address):
        self.input_first_name.fill(first_name)
        self.input_last_name.fill(last_name)
        self.input_phone.fill(phone)
        self.input_email.fill(email)
        self.input_empid.fill(empid)
        self.input_address.fill(address)

        # Navigate next and save
        self.btn_next.click()
        time.sleep(1)
        self.btn_next.click()
        self.btn_done.click()

    def add_personnel(self, firstname, lastname, phone, email, empid, address):
        """Full workflow to add personnel"""
        self.navigate_to_personnel()
        self.select_org_type()
        self.select_location()
        self.fill_personnel_details(firstname, lastname, phone, email, empid, address)

    def select_org_types(self, org_type: str):
        self.dropdown_org_type.click()
        self.page.get_by_role("option", name=org_type).click()

    def navigate_and_select_location(self, org_type="Governance"):
        self.btn_get_started.click()
        self.btn_personnel.click()
        self.btn_add_personnel.click()
        self.dropdown_org_type.click()
        if org_type.lower() == "governance":
            self.option_governance.click()
        else:
            self.option_administrator.click()

        # Step 3: Select Location
        self.btn_next.click()
        self.cmb_country.click()
        self.option_india.click()
        self.cmb_state.click()
        self.option_telangana.click()
        self.cmb_city.click()
        self.option_hyderabad.click()
        self.cmb_area.click()
        self.option_hydcity.click()

    def assign_institution_admin(self, institution_name: str):
       
        self.btn_get_started.click()
        self.btn_personnel.click()
        self.btn_add_personnel.click()

        self.dropdown_org_type.click()
        self.option_administrator.click()
        self.profile_admin.click()

        self.btn_next.click()

        self.cmb_institution.click()
        self.page.get_by_role("option", name=institution_name).click()

    def edit_personnel(self, search_name: str, updated_last_name: str):
    # Step 1: Navigate to Personnel
        self.btn_get_started.click()
        self.btn_personnel.click()
        self.input_search_personnel.click()
        self.input_search_personnel.fill(search_name)
        self.btn_edit_personnel_icon.click()
        self.txt_edit_personnel_header.wait_for()
        self.input_last_name_edit.click()
        self.input_last_name_edit.fill(updated_last_name)
        self.btn_edit_personnel_submit.click()

    def view_personnel(self, search_name: str):
        self.btn_get_started.click()
        self.btn_personnel.click()
        self.input_search_personnel.click()
        self.input_search_personnel.fill(search_name)
        self.btn_view_personnel.click()
        self.btn_close_view.click()
       
