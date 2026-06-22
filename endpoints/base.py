import allure
import pytest
import requests
import os


class Base:
    def __init__(self):
        self.json = None
        self.session = requests.Session()
        self.base_url = os.getenv('API_BASE_URL')
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

    @allure.step('Check status is 422 Unprocessable Entity')
    def check_status_unprocessable(self):
        return self.check_status_code(422)


    @allure.step('Check that user is unauthorized')
    def check_that_user_is_unauthorized(self):
        return self.check_status_code(401)


    @allure.step('Check that status is bad request')
    def check_that_status_is_bad_request(self):
        assert self.response.status_code == 400


    @allure.step('Check meme data matches expected')
    def check_meme_data(self, expected_meme):
        assert self.json is not None, "Response JSON is None"
        assert self.json['text'] == expected_meme['text'], \
            f"Text mismatch. Expected: {expected_meme['text']}, Got: {self.json['text']}"
        assert self.json['url'] == expected_meme['url'], \
            f"URL mismatch. Expected: {expected_meme['url']}, Got: {self.json['url']}"
        assert self.json['tags'] == expected_meme['tags'], \
            f"Tags mismatch. Expected: {expected_meme['tags']}, Got: {self.json['tags']}"
        assert self.json['info'] == expected_meme['info'], \
            f"Info mismatch. Expected: {expected_meme['info']}, Got: {self.json['info']}"
        return self

    @allure.step('Check meme updated correctly')
    def check_meme_updated(self, expected_text, expected_tags, meme_id):
        assert self.json is not None, "Response JSON is None"
        assert self.json['text'] == expected_text, \
            f"Text not updated. Expected: {expected_text}, Got: {self.json['text']}"
        assert self.json['id'] == str(meme_id), \
            f"ID changed. Expected: {meme_id}, Got: {self.json['id']}"
        assert self.json['tags'] == expected_tags, \
            f"Tags mismatch. Expected: {expected_tags}, Got: {self.json['tags']}"
        return self

    @allure.step('Check that tag exists in meme')
    def check_tag_exists(self, tag):
        assert self.json is not None, "Response JSON is None"
        assert tag in self.json['tags'], f"Tag '{tag}' not found in {self.json['tags']}"
        return self


    @allure.step('Get user name')
    def get_user(self):
        return self.response.json().get("user")