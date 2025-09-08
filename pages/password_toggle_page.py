from playwright.sync_api import Page
from base.base_page import BasePage

class PasswordTogglePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.tab_login = page.get_by_role("tab", name="Login/Signin")
        self.input_password = page.get_by_role("textbox", name="Enter Password")
        self.btn_toggle_password = page.get_by_role("button", name="toggle password visibility")

    def click_login_tab(self):
        self.tab_login.click()

    def enter_password(self, password: str):
        self.input_password.fill(password)

    def toggle_password_visibility(self):
        self.btn_toggle_password.click()

    def click_forgot_password(self):
        self.btn_forgot_password.click()

    def perform_password_toggle_test(self, password: str) -> bool:
        """Perform the password toggle: show → hide"""
        try:
            self.click_login_tab()
            self.enter_password(password)
            self.toggle_password_visibility()  # Show password
            self.toggle_password_visibility()  # Hide password
            return True
        except Exception:
            return False
