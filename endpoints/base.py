import allure
import requests


class Base:
    def __init__(self):
        self.json = None
        self.session = requests.Session()
        self.base_url = "http://memesapi.course.qa-practice.com"
        self.response = None

    @allure.step('Get headers')
    def _get_headers(self, token=None):
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = token
        return headers


    @allure.step('Get meme id')
    def get_id(self):
        return self.response.json().get("id")


    @allure.step('Get text of meme from response')
    def get_text(self):
        return self.response.json().get("text")


    @allure.step('Get url from response')
    def get_url(self):
        return self.response.json().get("url")


    @allure.step('Get tags of meme from response')
    def get_tags(self):
        return self.response.json().get("tags")


    @allure.step('Get info about meme from response')
    def get_info(self):
        return self.response.json().get("info")


    @allure.step('Check that meme id is correct')
    def check_meme_id_is_correct(self):
        assert self.json['id'] == self.get_id()


    @allure.step('Check that text of meme is correct')
    def check_text_is_correct(self):
        assert self.json['text'] == self.get_text()


    @allure.step('Check that tags of meme are correct')
    def check_tags_are_correct(self):
        assert self.json['tags'] == self.get_tags()


    @allure.step('Check that info about meme is response')
    def check_info_is_correct(self):
        assert self.json['info'] == self.get_info()


    @allure.step('Check status is 200')
    def check_status_is_ok(self):
        return self.check_status_code(200)


    @allure.step('Check status is 404')
    def check_status_not_found(self):
        return self.check_status_code(404)

    @allure.step('Check status code')
    def check_status_code(self, expected_code: int):
        assert self.response.status_code == expected_code, \
            f"Expected status {expected_code}, got {self.response.status_code}"
        return self
