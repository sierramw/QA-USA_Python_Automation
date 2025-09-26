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


        # Step 2: Check URL reachability only
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            # Handle the case when the server is not reachable
            print("Server is not reachable")

    # --- Test 1: Set addresses ---
    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutes(self.driver)

        routes_page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)

        assert routes_page.get_from_value() == data.ADDRESS_FROM
        assert routes_page.get_to_value() == data.ADDRESS_TO

    # --- Test 2: Select Supportive plan ---
    def test_select_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutes(self.driver)

        # PREREQUISITES
        routes_page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.call_taxi()

        routes_page.select_supportive_plan()
        assert routes_page.get_selected_plan_text() == "Supportive"

    # --- Test 3: Phone number + SMS verification ---
    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutes(self.driver)

        # PREREQUISITES
        routes_page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.call_taxi()

        routes_page.enter_phone_and_confirm(data.PHONE_NUMBER, helpers.retrieve_phone_code)
        assert routes_page.get_entered_phone_number() == data.PHONE_NUMBER

    # --- Test 4: Card details ---
    def test_fill_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutes(self.driver)

        # PREREQUISITES
        routes_page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.call_taxi()

        routes_page.open_payment_and_add_card(data.CARD_NUMBER, data.CARD_CODE)
        assert routes_page.get_payment_method_text() == "Card"

    # --- Test 5: Comment for driver ---
    def test_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutes(self.driver)

        # PREREQUISITES
        routes_page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.call_taxi()

        routes_page.add_comment(data.MESSAGE_FOR_DRIVER)
        assert routes_page.get_comment_text() == data.MESSAGE_FOR_DRIVER

    # --- Test 6: Blanket option ---
    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutes(self.driver)

        # PREREQUISITES
        routes_page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.call_taxi()

        routes_page.toggle_blanket()
        assert routes_page.is_blanket_selected()

    # --- Test 7: Ice creams ---
    def test_order_for_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutes(self.driver)

        # PREREQUISITES
        routes_page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.call_taxi()
        routes_page.select_supportive_plan()

        count = routes_page.add_icecreams(count=2)
        assert count == '2'

    # --- Test 8: Car search modal ---
    def test_car_search_modal_appears(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutes(self.driver)

        # PREREQUISITES
        routes_page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.call_taxi()
        routes_page.add_comment(data.MESSAGE_FOR_DRIVER)

        routes_page.place_order()
        assert routes_page.is_car_search_modal_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()