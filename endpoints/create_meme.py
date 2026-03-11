from endpoints.base import Base
import allure


class CreateMeme(Base):
    @allure.step('Create meme')
    def create_meme(self, meme_data, token):
        url_endpoint = f"{self.base_url}/meme"
        headers = self._get_headers(token)
        self.response = self.session.post(url_endpoint, json=meme_data, headers=headers)
        self.json = self.response.json()
        return self
