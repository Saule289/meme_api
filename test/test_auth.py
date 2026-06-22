import pytest
import allure

from conftest import token
from endpoints.authorize import Authorize
import os

@allure.feature('Authorization')
class TestAuthorization:

    def test_auth_success(self):
        username = os.getenv('API_USERNAME')
        auth = Authorize()
        auth.authorize_user(username)
        auth.check_status_is_ok()

        token_value = auth.get_token()
        auth.check_token_valid(token_value)

    @allure.story('Negative login')
    @allure.story('Negative login - wrong username')
    def test_auth_wrong_username(self):
        auth = Authorize()
        auth.authorize_user("wrong_user")
        auth.check_status_code(401)


    @allure.story('Negative login - empty username')
    def test_auth_empty_username(self):
        auth = Authorize()
        auth.authorize_user("")
        auth.check_status_code(400)


    @allure.story('Token validation')
    def test_invalid_token_returns_401(self, create_meme, new_meme):
        create_meme.create_meme(new_meme, token="invalid_token_12345")
        create_meme.check_status_code(401)

    @allure.story('Token validation - no token')
    def test_no_token_returns_401(self, create_meme, new_meme):
        create_meme.create_meme(new_meme, token=None)
        create_meme.check_status_code(401)