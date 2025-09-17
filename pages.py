from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutes:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

        # --- Address fields ---
        self.FROM_FIELD = (By.ID, "from")
        self.TO_FIELD = (By.ID, "to")
        self.CALL_TAXI_BTN = (By.CLASS_NAME, "button")

        # --- Tariff selection ---
        self.SUPPORTIVE_TARIFF = (By.XPATH, "//div[contains(text(),'Supportive')]")

        # --- Phone number flow ---
        self.PHONE_FIELD = (By.CSS_SELECTOR, "input#phone")
        self.NEXT_BTN = (By.XPATH, "//button[text()='Next']")
        self.SMS_CODE_INPUT = (By.CSS_SELECTOR, "input#code")
        self.CONFIRM_PHONE_BTN = (By.XPATH, "//button[text()='Confirm']")

        # --- Card payment flow ---
        self.PAYMENT_METHOD_BTN = (By.XPATH, "//div[contains(@class,'pp-button')]")
        self.ADD_CARD_BTN = (By.XPATH, "//div[contains(text(),'Add card')]")
        self.CARD_NUMBER_INPUT = (By.CSS_SELECTOR, "input#number")
        self.CVV_INPUT = (By.CSS_SELECTOR, "input#code")
        self.LINK_CARD_BTN = (By.XPATH, "//button[text()='Link']")
        self.CARD_CONFIRMATION = (By.XPATH, "//div[contains(text(),'Card')]")

        # --- Comment & extras ---
        self.COMMENT_FIELD = (By.ID, "comment")
        self.BLANKET_CHECKBOX = (By.NAME, "blanket")
        self.ICECREAM_ADD_BTN = (By.XPATH, "//button[contains(.,'Ice cream')]")

        # --- Final order ---
        self.ORDER_BTN = (By.XPATH, "//button[text()='Call a Taxi']")
        self.CAR_SEARCH_MODAL = (By.CLASS_NAME, "order-modal")

    # --- Step 1: Set address ---
    def set_address(self, from_address, to_address):
        from_field = self.wait.until(EC.element_to_be_clickable(self.FROM_FIELD))
        from_field.clear()
        from_field.send_keys(from_address)

        to_field = self.wait.until(EC.element_to_be_clickable(self.TO_FIELD))
        to_field.clear()
        to_field.send_keys(to_address)

    def click_call_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BTN)).click()

    # --- Step 2: Select tariff ---
    def select_supportive_plan(self):
        self.wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_TARIFF)).click()

    # --- Step 3: Phone number flow ---
    def enter_phone_and_confirm(self, phone, code_callback):
        field = self.wait.until(EC.element_to_be_clickable(self.PHONE_FIELD))
        field.clear()
        field.send_keys(phone)
        self.driver.find_element(*self.NEXT_BTN).click()

        # simulate retrieving code (via callback helper)
        code = code_callback()
        sms_field = self.wait.until(EC.element_to_be_clickable(self.SMS_CODE_INPUT))
        sms_field.send_keys(code)
        self.driver.find_element(*self.CONFIRM_PHONE_BTN).click()

    # --- Step 4: Card payment flow ---
    def open_payment_and_add_card(self, card_number, cvv):
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_METHOD_BTN)).click()
        self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_BTN)).click()

        card_field = self.wait.until(EC.element_to_be_clickable(self.CARD_NUMBER_INPUT))
        card_field.clear()
        card_field.send_keys(card_number)

        cvv_field = self.wait.until(EC.element_to_be_clickable(self.CVV_INPUT))
        cvv_field.clear()
        cvv_field.send_keys(cvv)

        self.wait.until(EC.element_to_be_clickable(self.LINK_CARD_BTN)).click()
        self.wait.until(EC.presence_of_element_located(self.CARD_CONFIRMATION))

    def get_payment_method_text(self):
        return self.driver.find_element(*self.CARD_CONFIRMATION).text

    # --- Step 5: Add comment ---
    def add_comment(self, message):
        field = self.wait.until(EC.element_to_be_clickable(self.COMMENT_FIELD))
        field.clear()
        field.send_keys(message)

    # --- Step 6: Toggle blanket ---
    def toggle_blanket(self):
        self.wait.until(EC.element_to_be_clickable(self.BLANKET_CHECKBOX)).click()

    # --- Step 7: Add ice creams ---
    def add_icecreams(self, count=2):
        button = self.wait.until(EC.element_to_be_clickable(self.ICECREAM_ADD_BTN))
        for i in range(count):
            button.click()
        return count

    # --- Step 8: Place order ---
    def place_order(self):
        self.wait.until(EC.element_to_be_clickable(self.ORDER_BTN)).click()

    def is_car_search_modal_displayed(self):
        modal = self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL))
        return modal.is_displayed()
