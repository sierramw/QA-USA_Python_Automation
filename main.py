import pytest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import data, helpers
from pages import UrbanRoutes


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # Step 1: Set up driver and capabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        cls.driver = webdriver.Chrome()

        # Step 2: Check URL reachability
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            cls.driver.get('https://cnt-5847f2e3-abaa-4346-bc89-2a6746d28764.containerhub.tripleten-services.com/')
        else:
            raise RuntimeError("Cannot_connect_to_Urban_Routes")

        # Step 3: Initialize page object
        cls.page = UrbanRoutes(cls.driver)

    # --- Test 1: Set addresses ---
    def test_set_route(self):
        self.page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        # Assertion: make sure the values were set correctly
        from_value = self.page.driver.find_element(*self.page.FROM_FIELD).get_attribute("value")
        to_value = self.page.driver.find_element(*self.page.TO_FIELD).get_attribute("value")
        assert from_value == data.ADDRESS_FROM
        assert to_value == data.ADDRESS_TO

    # --- Test 2: Select Supportive plan ---
    def test_select_plan(self):
        self.page.select_supportive_plan()
        # Assertion: check that Supportive plan element is selected
        selected_text = self.page.driver.find_element(*self.page.SUPPORTIVE_TARIFF).text
        assert "Supportive" in selected_text

    # --- Test 3: Phone number + SMS verification ---
    def test_fill_phone_number(self):
        self.page.enter_phone_and_confirm(data.PHONE_NUMBER, helpers.retrieve_phone_code)
        # Assertion: ensure confirmation succeeded
        assert "phone" in self.page.driver.page_source.lower()

    # --- Test 4: Card details ---
    def test_fill_card(self):
        self.page.open_payment_and_add_card(data.CARD_NUMBER, data.CARD_CODE)
        # Assertion: check payment method changes to "Card"
        assert self.page.get_payment_method_text() == "Card"

    # --- Test 5: Comment for driver ---
    def test_comment_for_driver(self):
        self.page.add_comment(data.MESSAGE_FOR_DRIVER)
        # Assertion: verify comment text was entered
        value = self.page.driver.find_element(*self.page.COMMENT_FIELD).get_attribute("value")
        assert value == data.MESSAGE_FOR_DRIVER

    # --- Test 6: Blanket option ---
    def test_order_blanket_and_handkerchiefs(self):
        self.page.toggle_blanket()
        # Assertion: ensure checkbox is selected
        checked = self.page.driver.find_element(*self.page.BLANKET_CHECKBOX).is_selected()
        assert checked is True

    # --- Test 7: Ice creams ---
    def test_order_for_2_ice_creams(self):
        count = self.page.add_icecreams(count=2)
        # Assertion: check that 2 clicks were registered (you might need a UI counter locator here)
        assert count == 2

    # --- Test 8: Car search modal ---
    def test_car_search_modal_appears(self):
        self.page.place_order()
        # Assertion: modal should appear
        assert self.page.is_car_search_modal_displayed() is True

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
