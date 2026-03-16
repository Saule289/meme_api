from endpoints.base import Base
import allure


class CreateMeme(Base):
    @allure.step('Create meme')
    def create_meme(self, meme_data, token):
        url_endpoint = f"{self.base_url}/meme"
        headers = self._get_headers(token)
        self.response = self.session.post(url_endpoint, json=meme_data, headers=headers)

        if self.response.status_code in [200, 201]:
            try:
                self.json = self.response.json()
            except:
                self.json = None
        else:
            self.json = None
            print(f"Create meme failed with status {self.response.status_code}")

        return self
