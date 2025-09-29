from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import helpers


class UrbanRoutes:
    # --- Address fields ---
    FROM_FIELD = (By.ID, "from")
    TO_FIELD = (By.ID, "to")
    CALL_TAXI_BTN = (By.XPATH, "//button[text()='Call a taxi']")

    # --- Tariff selection ---
    SUPPORTIVE_TARIFF = (By.XPATH, "//div[contains(text(),'Supportive')]")

    # --- Phone number flow ---
    PHONE_FIELD = (By.XPATH, '//div[text()="Phone number"]')
    NEXT_BTN = (By.XPATH, "//button[text()='Next']")
    SMS_CODE_INPUT = (By.CSS_SELECTOR, "input#code")
    CONFIRM_PHONE_BTN = (By.XPATH, "//button[text()='Confirm']")
    PHONE_NUMBER_BTN = (By.CLASS_NAME, "np-text")
    ENTER_PHONE_FIELD = (By.ID, 'phone')

    # --- Card payment flow ---
    PAYMENT_METHOD_BTN = (By.XPATH, '//div[@class="pp-button filled"]')
    ADD_CARD_BTN = (By.XPATH, "//div[text()='Add card']")
    CARD_NUMBER_INPUT = (By.CSS_SELECTOR, "input#number")
    CVV_INPUT = (By.XPATH, "(//input[@id='code'])[2]")
    LINK_CARD_BTN = (By.XPATH, "//button[text()='Link']")
    CARD_CONFIRMATION = (By.XPATH, "//div[contains(text(),'Card')]")

    # --- Comment & extras ---
    COMMENT_FIELD = (By.ID, "comment")
    BLANKET_CHECKBOX = (By.XPATH, "//input[@class='switch-input']")
    BLANKET_TOGGLE = (By.XPATH, "//div[@class='switch']")
    ICECREAM_ADD_BTN = (By.XPATH, '//div[text()="+"]')
    ICECREAM_ADD_QTY = (By.XPATH, "//div[@class='counter-value']")

    # --- Final order ---
    ORDER_BTN = (By.XPATH, '//span[@class="smart-button-main"]')
    CAR_SEARCH_MODAL = (By.XPATH, '//div[@class="order-header-title"]')
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # --- Step 1: Set address ---
    def set_address(self, from_address, to_address):
        from_field = self.wait.until(EC.element_to_be_clickable(self.FROM_FIELD))
        from_field.clear()
        from_field.send_keys(from_address)

        to_field = self.wait.until(EC.element_to_be_clickable(self.TO_FIELD))
        to_field.clear()
        to_field.send_keys(to_address)

    def get_from_value(self):
        return self.driver.find_element(*self.FROM_FIELD).get_attribute("value")

    def get_to_value(self):
        return self.driver.find_element(*self.TO_FIELD).get_attribute("value")

    # --- Step 1.5: Call taxi ---
    def call_taxi(self):
            #Click the 'Call a taxi' button after addresses are set
            button = self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BTN))
            button.click()

    # --- Step 2: Select tariff ---
    def select_supportive_plan(self):
        self.wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_TARIFF)).click()

    def get_selected_plan_text(self):
        return self.driver.find_element(*self.SUPPORTIVE_TARIFF).text

    # --- Step 3: Phone number flow ---
    def enter_phone_and_confirm(self, phone, code_callback):
        # Click the "Phone number" div button
        self.driver.find_element(*self.PHONE_FIELD).click()

        # Enter phone number in the input field
        field = self.driver.find_element(*self.ENTER_PHONE_FIELD)
        field.send_keys(phone)

        self.driver.find_element(*self.NEXT_BTN).click()

        # simulate retrieving code (via callback helper)
        code = helpers.retrieve_phone_code(self.driver)
        sms_field = self.wait.until(EC.element_to_be_clickable(self.SMS_CODE_INPUT))
        sms_field.send_keys(code)
        self.driver.find_element(*self.CONFIRM_PHONE_BTN).click()

    def get_entered_phone_number(self):
        return self.driver.find_element(*self.PHONE_NUMBER_BTN).text

    # --- Step 4: Card payment flow ---
    def open_payment_and_add_card(self, card_number, cvv):
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_METHOD_BTN)).click()
        # Debug: Print all elements that contain "Add card"
        elements = self.driver.find_elements(By.XPATH, "//*[contains(text(),'Add card')]")
        print(f"Found {len(elements)} elements with 'Add card' text")
        for elem in elements:
            print(f"Tag: {elem.tag_name}, Text: {elem.text}")
        self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_BTN)).click()

        card_field = self.wait.until(EC.element_to_be_clickable(self.CARD_NUMBER_INPUT))
        card_field.clear()
        card_field.send_keys(card_number)

        cvv_field = self.wait.until(EC.element_to_be_clickable(self.CVV_INPUT))
        cvv_field.clear()
        cvv_field.send_keys(cvv)
        from selenium.webdriver.common.keys import Keys
        cvv_field.send_keys(Keys.TAB)
        self.wait.until(EC.element_to_be_clickable(self.LINK_CARD_BTN)).click()
        self.wait.until(EC.presence_of_element_located(self.CARD_CONFIRMATION))

    def get_payment_method_text(self):
        return self.driver.find_element(*self.CARD_CONFIRMATION).text

    # --- Step 5: Add comment ---
    def add_comment(self, message):
        field = self.wait.until(EC.element_to_be_clickable(self.COMMENT_FIELD))
        field.clear()
        field.send_keys(message)

    def get_comment_text(self):
        return self.driver.find_element(*self.COMMENT_FIELD).get_attribute("value")

    BLANKET_TOGGLE = (By.CSS_SELECTOR, ".slider.round")
    # --- Step 6: Toggle blanket ---
    def toggle_blanket(self):
        # Debug: Look for blanket-related elements
        elements = self.driver.find_elements(By.XPATH, "//*[contains(@id,'blanket') or contains(text(),'Blanket')]")
        print(f"Found {len(elements)} blanket-related elements")
        for elem in elements:
            print(f"Tag: {elem.tag_name}, ID: {elem.get_attribute('id')}, Text: {elem.text}")
        self.wait.until(EC.element_to_be_clickable(self.BLANKET_TOGGLE)).click()

    def is_blanket_selected(self):
        return self.driver.find_element(*self.BLANKET_CHECKBOX).get_property("checked")

     # --- Step 7: Add ice creams ---
    def add_icecreams(self, count=2):
        button = self.wait.until(EC.element_to_be_clickable(self.ICECREAM_ADD_BTN))
        for i in range(count):
            button.click()
        return self.wait.until(EC.element_to_be_clickable(self.ICECREAM_ADD_QTY)).text

   # --- Step 8: Place order ---
    def place_order(self):
        self.wait.until(EC.element_to_be_clickable(self.ORDER_BTN)).click()

    def is_car_search_modal_displayed(self):
        modal = self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL))
        return modal.is_displayed()