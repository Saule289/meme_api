from endpoints.base import Base
import allure

class CheckToken(Base):
    @allure.step("Check the token")
    def check_token(self, token):
        url = f"{self.base_url}/authorize/{token}"
        self.response = self.session.get(url)
        if self.response.status_code == 200:
            try:
                self.json = self.response.json()
            except:
                self.json = None
        else:
            self.json = None

        return self


    @allure.step("Get the username from response")
    def get_username_from_response(self):
        if not self.json:
            return None
        return self.json.get('user') or self.json.get('username')

    @allure.step("Check that token is valid")
    def is_token_valid(self, expected_username=None):
        if self.response.status_code != 200:
            return False
        if expected_username is None:
            return True
        return self.get_username_from_response() == expected_username
