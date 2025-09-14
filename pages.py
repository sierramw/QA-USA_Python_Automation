from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Create classes for both tests
# python

class UrbanRoutes:
    def __init__ (self, driver, timeout=7):
        # code here
            FROM_FIELD = (By.ID, "from")
            TO_FIELD = (By.ID, "to")
            CALL_TAXI_BTN = (By.CLASS_NAME, "button")
            SUPPORTIVE_TARIFF = (By.XPATH, "//div[contains (text (), ‘Supportive’)]")
            PHONE_INPUT = (By.CSS_SELECTOR, "input#phone")
            COMMENT_FIELD = (By.ID, "comment")
            BLANKET_CHECKBOX = (By.NAME, "blanket")
            ICECREAM_ADD_BTN = (By.XPATH, "//button[contains(.,‘Ice cream’)]")
            ORDER_BTN = (By.XPATH, "//button[text()='Call a Taxi']")

    def set_address (self, from_address, to_address) :
        from_field = self.wait.until (EC.element_to_be_clickable (self.FROM_FIELD))
        from_field.clear()
        from_field.send_keys (from_address)
        to_field=self.wait.until (EC.element_to_be_clickable (self.TO_FIELD))
        to_field.clear()
        to_field.send_keys (to_address)

    def click_call_taxi (self) :
        self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BTN)).click()

    def select_supportive_plan (self) :
        self.wait.until (EC.element_to_be_clickable (self.SUPPORTIVE_TARIFF)).click()

    def enter_phone (self, phone) :
        field = self.wait.until (EC.element_to_be_clickable (self.PHONE_INPUT))
        field.clear()
        field.send_keys (phone)

    def add_comment (self, message) :
        field = self.wait.until (EC.element_to_be_clickable (self.COMMENT_FIELD))
        field.clear()
        field.send_keys (message)

    def toggle_blanket (self) :
        self.wait.until (EC.element_to_be_clickable (self.BLANKET_CHECKBOX)).click()

    def add_icecreams (self, count=2) :
        button = self.wait.until (EC.element_to_be_clickable (self.ICECREAM_ADD_BTN))
        for i in range(count) :
            button.click()

    def place_order (self) :
        self.wait.until (EC.element_to_be_clickable (self.ORDER_BTN)).click()