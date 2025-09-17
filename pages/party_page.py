from playwright.sync_api import Page

class PartyPage:
    def __init__(self, page: Page):
        self.page = page
        self.get_started_btn = page.get_by_role("button", name="Get Started")
        self.party_btn = page.get_by_role("button", name="Party")
        self.add_party_btn = page.get_by_role("button", name="+ Add Party")
        # 🎯 target only file input, not label or button
        self.logo_input = page.locator("input[type='file']")
        self.name_input = page.get_by_role("textbox").first
        self.code_input = page.get_by_role("textbox").nth(1)
        self.next_btn = page.get_by_role("button", name="Next")
        self.back_to_home_btn = page.get_by_role("button", name="Back to Home")

        self.search_party_input = page.get_by_role("textbox", name="Search Party")
        self.more_option_btn = page.get_by_role("button", name="primaryMoreOption").first
        self.edit_icon_btn = page.get_by_role("button", name="primaryEditIcon").first
        self.edit_party_btn = page.get_by_role("button", name="Edit Party")
        self.apply_button = page.get_by_role("button", name="Apply")
        self.view_icon = page.get_by_role("button", name="primaryEyeIcon").first
        self.close_button = page.get_by_role("button", name="Close")


    def navigate_party_section(self):
        self.get_started_btn.click()
        self.party_btn.click()

    def add_party(self, logo_file, party_name, party_code, country, state, district, city):
        self.add_party_btn.click()

        self.logo_input.set_input_files(logo_file)

        self.name_input.fill(party_name)
        self.code_input.fill(str(party_code))

        self.next_btn.click()
        self.page.get_by_role("combobox").click()
        self.page.get_by_role("option", name=country).click()
        self.page.get_by_role("combobox").nth(1).click()
        self.page.get_by_role("option", name=state).click()
        self.page.get_by_role("combobox").nth(2).click()
        self.page.get_by_role("option", name=district).click()
        # self.page.get_by_role("combobox").nth(3).click()
        # self.page.get_by_role("option", name=city).click()

        # Final steps
        self.next_btn.click()
        self.next_btn.click()
        self.back_to_home_btn.click()

    def edit_party(self, search_text: str, updated_name: str):
        """Edit existing party details"""
        self.search_party_input.click()
        self.search_party_input.fill(search_text)
        self.edit_icon_btn.click()
        self.name_input.click()
        self.name_input.press("ArrowRight")
        self.name_input.fill(updated_name)

        self.edit_party_btn.click()

    def view_party(self):
        self.view_icon.click()
        self.close_button.click()


    def navigate_party_sections(self, country: str, state: str, district: str, city: str = None):
        self.get_started_btn.click()
        self.party_btn.click()
        self.page.get_by_role("combobox").nth(0).click()
        self.page.get_by_role("option", name=country).click()

        self.page.get_by_role("combobox").nth(1).click()
        self.page.get_by_role("option", name=state).click()

        self.page.get_by_role("combobox").nth(2).click()
        self.page.get_by_role("option", name=district).click()

    # # Step 5: Select City (optional)
    #     if city:
    #         self.page.get_by_role("combobox").nth(3).click()
    #         self.page.get_by_role("option", name=city).click()

        self.page.get_by_role("button", name="Apply").click()
