import pytest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import data, helpers
from pages import UrbanRoutes

class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # Step 1: Set up driver and capabilities
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        cls.driver = webdriver.Chrome()

        # Step 2: Check URL reachability
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            cls.driver.get('https://cnt-bc9f1539-ce05-494f-92d1-b3d288cc257d.containerhub.tripleten-services.com/')
        else:
            raise RuntimeError("Cannot_connect_to_Urban_Routes")

        # Step 3: Initialize page object
        cls.page = UrbanRoutes(cls.driver)

    def test_set_route(self):
            self.page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
            assert routes.page.get_from_address(data.ADDRESS_FROM) == data.ADDRESS_TO
            assert routes.page.get_to_address() == data.ADDRESS_TO

    def test_select_plan(self):
            self.page.add_comment(data.MESSAGE_FOR_DRIVER)
            self.page.select_supportive_plan()

    def test_fill_phone_number(self):
            self.page.enter_phone(data.PHONE_NUMBER)
            # Here you’d add helpers.retrieve_phone_code () to finish confirmation

    def test_fill_card (self):
            # Step 1-2: Set addresses
            self.page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)

            # Step 3: Click "Call a Taxi" button
            self.page.click_call_taxi_button()

            # Step 4: Click on the Supportive plan option
            self.page.click_supportive_plan()

            # Step 5: Click on Payment Method
            self.page.click_payment_method()

            # Step 6: Click on Add Card
            self.page.click_add_card()

            # Step 7: Enter valid Card Number and Code
            self.page.enter_card_details(data.CARD_NUMBER, data.CARD_CODE)

            # Step 8: Use TAB or simulate click outside to change focus
            self.page.change_focus_from_code_field()

            # Step 9: Ensure "Link" button becomes clickable
            # (This might be handled automatically or you might need to wait)

            # Step 10: Click "Link"
            self.page.click_link_button()

            # Step 11: Assert that payment method text changes from "Cash" to "Card"
            assert self.page.get_payment_method_text() == "Card"

    def test_comment_for_driver(self):
            self.page.add_comment(data.MESSAGE_FOR_DRIVER)

    def test_order_blanket_and_handkerchiefs(self):
            self.page.toggle_blanket()

    def test_order_for_2_ice_creams(self):
            for i in range(2):
                self.page.add_ice_cream()
                # 1. Find the ice cream add button
                # 2. Increment_ice_cream()

    def test_car_search_model_appears(self):
            self.page.place_order()
            # assert modal is visible here

    @classmethod
    def teardown_class(cls):
            cls.driver.quit()