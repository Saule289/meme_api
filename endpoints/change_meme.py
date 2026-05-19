from endpoints.base import Base
import allure

class ChangeMeme(Base):
    @allure.step("Change meme information")
    def update_meme(self, meme_id, text, url, tags, info, token):
        url_endpoint = f"{self.base_url}/meme/{meme_id}"
        headers = self._get_headers(token)
        payload = \
        {
            "id": meme_id,
            "text": text,
            "url": url,
            "tags": tags,
            "info": info
        }
        self.response = self.session.put(url_endpoint, json=payload, headers=headers)
        if self.response.status_code in [200, 201]:
            try:
                self.json = self.response.json()
            except:
                self.json = None
        else:
            self.json = None

        return self
