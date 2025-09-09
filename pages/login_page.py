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
        self.otp_inputs = page.locator("input[type='text'][maxlength='1']")
        self.countdown_text = page.locator("p.MuiTypography-body1.field-link")
        self.resend_button = page.locator("button:has-text('Resend')")
        self.masked_email = page.locator("span.MuiFormControlLabel-label", has_text="Email:")
        self.btn_get_started = page.get_by_role("button", name="Get Started")
        self.btn_admin_menu = page.get_by_role("button", name="Admin")  # top-right user menu
        self.tab_settings = page.locator("button[role='tab']", has_text="Settings")
        self.tab_account_settings = page.get_by_role("tab", name="Account Settings")

        # --- Logout button inside Account Settings ---
        self.btn_logout = page.get_by_role("button", name="Click here to Logout")


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
