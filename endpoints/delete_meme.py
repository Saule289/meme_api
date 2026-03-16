from endpoints.base import Base
import allure

class DeleteMeme(Base):
    @allure.step('Delete meme by id')
    def delete_meme_by_id(self, meme_id, token):
        url = f"{self.base_url}/meme/{meme_id}"
        headers = self._get_headers(token)
        self.response = self.session.delete(url, headers=headers)
        return self
