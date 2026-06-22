from endpoints.base import Base
import allure

class Authorize(Base):
    @allure.step('Authorization of user')
    def authorize_user(self, name):
        url = f"{self.base_url}/authorize"
        payload = {"name": name}
        self.response = self.session.post(url, json=payload)
        return self


    @allure.step('Get token')
    def get_token(self):
        return self.response.json().get("token")


    @allure.step('Check token is valid via diagnostic endpoint')
    def check_token_valid(self, token):
        from endpoints.check_token import CheckToken
        check = CheckToken()
        check.check_token(token)
        check.check_status_code(200)
        return self




