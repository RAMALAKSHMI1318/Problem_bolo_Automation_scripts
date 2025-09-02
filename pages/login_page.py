from playwright.sync_api import Page, expect
from base.base_page import BasePage
import time

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.tab_login = page.get_by_role("tab", name="Login/Signin")
        self.input_email = page.get_by_role("textbox", name="Enter Email Address")
        self.input_password = page.get_by_role("textbox", name="Enter Password")
        self.btn_next = page.get_by_role("button", name="Next")
        self.btn_login = page.get_by_role("button", name="Log-in")



    def login(self, email: str, password: str):
        # Go to Login tab
        self.tab_login.click()

        # Fill credentials
        self.input_email.fill(email)
        self.input_password.fill(password)

        # First Next
        self.btn_next.click()

        # Wait before second Next
        expect(self.btn_next).to_be_enabled(timeout=10000)
        time.sleep(2)  # extra buffer
        self.btn_next.click()

        # Wait before Log-in
        expect(self.btn_login).to_be_visible(timeout=10000)
        self.btn_login.click()
