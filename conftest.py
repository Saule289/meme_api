import pytest


from endpoints.get_meme import GetMeme
from endpoints.create_meme import CreateMeme
from endpoints.delete_meme import DeleteMeme
from endpoints.change_meme import ChangeMeme
from endpoints.authorize import Authorize



@pytest.fixture()
def create_meme():
    return CreateMeme()


@pytest.fixture()
def delete_meme():
    return DeleteMeme()


@pytest.fixture()
def get_meme_by_id():
    return GetMeme()


@pytest.fixture()
def change_meme():
    return ChangeMeme()


@pytest.fixture()
def token():
    auth = Authorize()
    auth.authorize_user("saule").check_status_is_ok()
    token_value = auth.get_token()
    assert token_value is not None, "Токен не получен"
    return token_value