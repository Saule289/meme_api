import pytest
import allure
from endpoints.authorize import Authorize

@allure.feature('Authorization')
class TestAuthorization:

    @allure.story('Positive login')
    def test_auth_success(self):
        auth = Authorize()
        auth.authorize_user("saule")
        auth.check_status_is_ok()
        assert auth.get_token() is not None, "Token should be returned"

    @allure.story('Negative login')
    @pytest.mark.parametrize("username, expected_status", [
        ("", 200),
        ("wrong_user", 200),
        (None, 400),
        ("invalid", 200),
        ("any_string", 200),
    ])
    def test_auth_failure(self, username, expected_status):
        auth = Authorize()
        auth.authorize_user(username)
        assert auth.response.status_code == expected_status


    @allure.story('Token validation')
    def test_invalid_token(self, create_meme, new_meme):
        create_meme.create_meme(new_meme, token="invalid_token_12345")
        assert create_meme.response.status_code == 401

    @allure.story('Token validation - no token')
    def test_no_token_returns_401(self, create_meme, new_meme):
        create_meme.create_meme(new_meme, token=None)
        assert create_meme.response.status_code == 401