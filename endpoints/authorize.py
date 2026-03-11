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


    @allure.step('Get user name')
    def get_user(self):
        return self.response.json().get("user")


