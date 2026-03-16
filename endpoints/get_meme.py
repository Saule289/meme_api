from endpoints.base import Base
import allure


class GetMeme(Base):
    @allure.step('Get meme by id')
    def get_meme_by_id(self, meme_id, token):
        url = f"{self.base_url}/meme/{meme_id}"
        headers = self._get_headers(token)
        self.response = self.session.get(url, headers=headers)

        if self.response.status_code == 200:
            try:
                self.json = self.response.json()
            except:
                self.json = None
        else:
            self.json = None
            return self


    @allure.step('Get all memes')
    def get_meme(self,  token):
        url = f"{self.base_url}/meme"
        headers = self._get_headers(token)
        self.response = self.session.get(url, headers=headers)
        return self
