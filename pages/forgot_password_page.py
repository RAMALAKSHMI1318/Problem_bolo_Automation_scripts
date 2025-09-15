from base.base_page import BasePage
from playwright.sync_api import expect

class ForgotPasswordPage(BasePage):
    """Page object for Forgot Password functionality"""

    # ----------------- Locators -----------------
    LOGIN_TAB = "tab[name='Login/Signin']"
    FORGOT_PASSWORD_BUTTON = "button[name='Forgot Password?']"
    FORGOT_PASSWORD_HEADING = "text=Forgot Password"
    CROSS_BUTTON = "button:has(svg[data-testid='CloseIcon'])"
    
    MOBILE_INPUT = "input[placeholder='1 (702) 123-4567']"
    EMAIL_INPUT = "input[placeholder='Enter Registered Email Address']"
    OR_SEPARATOR = "text=Or"
    NEXT_BUTTON = "button:has-text('Next'):not([disabled])"  

     
    NEXT_BUTTON_DISABLED = "button:has-text('Next')"  
    RESEND_BUTTON = "button:has-text('Resend')"
    RESEND_OTP_BUTTON = "button:has-text('Resend OTP')"
    BACK_BUTTON = "button:has-text('Back')"
    NEW_PASSWORD_TAB_TEXT = "text='Enter New Password'"
    NEW_PASSWORD_INPUT = "input[placeholder='Enter New Password']"
    PASSWORD_EYE_ICON = "svg[data-testid='VisibilityIcon']"
    CONFIRM_PASSWORD_INPUT = "input[placeholder='Re-Enter Password']"
    REGISTER_BUTTON = "button:has-text('Register')"
    NEW_PASSWORD_EYE_ICON = "(//button[contains(@class,'MuiIconButton-root')])[1]"
    CONFIRM_PASSWORD_EYE_ICON = "(//button[contains(@class,'MuiIconButton-root')])[2]"
    BACK_BUTTON = "//button[normalize-space()='Back']"
    OTP_INPUTS = "input[type='text'][maxlength='1']"  # 4 OTP inputs
    BACK_TO_HOME_BUTTON = "button:has-text('Back to Home')"

    # ----------------- Actions -----------------
    def click_login_tab(self):
        self.page.get_by_role("tab", name="Login/Signin").click()

    def click_forgot_password_button(self):
        self.page.get_by_role("button", name="Forgot Password?").click()

    def is_heading_visible(self) -> bool:
        """Check if Forgot Password heading is visible"""
        locator = self.page.get_by_text("Forgot Password", exact=True)
        expect(locator).to_be_visible(timeout=5000)
        return locator.is_visible()

    def click_cross_button(self):
        self.page.get_by_role("button").first.click()  

    # ----------------- FPASS03 Actions -----------------
    def is_mobile_input_visible(self) -> bool:
        locator = self.page.locator(self.MOBILE_INPUT)
        expect(locator).to_be_visible(timeout=5000)
        return locator.is_visible()

    def is_email_input_visible(self) -> bool:
        locator = self.page.locator(self.EMAIL_INPUT)
        expect(locator).to_be_visible(timeout=5000)
        return locator.is_visible()

    def is_or_separator_visible(self) -> bool:
        locator = self.page.get_by_text("Or", exact=True)
        expect(locator).to_be_visible(timeout=5000)
        return locator.is_visible()

    def enter_mobile_number(self, mobile: str):
        locator = self.page.locator(self.MOBILE_INPUT)
        expect(locator).to_be_visible(timeout=5000)
        locator.fill(mobile)  

    
    
        self.page.wait_for_timeout(1000)


    def enter_email(self, email: str):
        """Fill email in input field"""
        locator = self.page.locator(self.EMAIL_INPUT)
        expect(locator).to_be_visible(timeout=5000)
        locator.fill(email)

    def click_next_button(self):
        """Click the enabled Next button"""
        locator = self.page.locator(self.NEXT_BUTTON)
        expect(locator).to_be_visible(timeout=5000)
        locator.click()

    def is_next_button_disabled(self):
        next_button = self.page.locator("button:has-text('Next')[disabled]")
        return next_button.count() == 1

    def is_resend_disabled(self):
        return self.page.locator(self.RESEND_BUTTON).get_attribute("disabled") is not None


    def is_resend_enabled(self):
        """Returns True if the Resend OTP button is enabled."""
        return self.page.locator(self.RESEND_OTP_BUTTON).is_enabled()

    def click_back_button(self):
        """Click the Back button."""
        self.page.locator(self.BACK_BUTTON).click()

    def enter_new_password(self, password):
        self.page.locator(self.NEW_PASSWORD_INPUT).fill(password)

    def toggle_password_visibility(self):
        self.page.locator(self.PASSWORD_EYE_ICON).first.click(force=True)

    def enter_confirm_password(self, password: str):
        confirm_input = self.page.locator(self.CONFIRM_PASSWORD_INPUT)
        confirm_input.fill(password)

    def is_register_button_enabled(self) -> bool:
        return self.page.locator(self.REGISTER_BUTTON).is_enabled()