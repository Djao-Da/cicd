import allure
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


@allure.feature("Login")
class TestLogin:

    @allure.title("Valid user can log in successfully")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_login_valid_user(self, page: Page):
        login = LoginPage(page)
        login.open()
        login.login("standard_user", "secret_sauce")
        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    @allure.title("Locked out user sees error message")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_login_locked_out_user(self, page: Page):
        login = LoginPage(page)
        login.open()
        login.login("locked_out_user", "secret_sauce")
        expect(login.error_message).to_be_visible()
        assert "locked out" in login.get_error_message().lower()

    @allure.title("Wrong password shows error message")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_login_wrong_password(self, page: Page):
        login = LoginPage(page)
        login.open()
        login.login("standard_user", "wrong_password")
        expect(login.error_message).to_be_visible()
        assert "username and password do not match" in login.get_error_message().lower()

    @allure.title("Empty credentials shows error message")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_login_empty_credentials(self, page: Page):
        login = LoginPage(page)
        login.open()
        login.login("", "")
        expect(login.error_message).to_be_visible()
        assert "username is required" in login.get_error_message().lower()
