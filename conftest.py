import pytest
from endpoints.get_meme import GetMeme
from endpoints.create_meme import CreateMeme
from endpoints.delete_meme import DeleteMeme
from endpoints.change_meme import ChangeMeme
from endpoints.authorize import Authorize


NEW_MEME_DATA = {
    "text": "Why this is so",
    "url": "https://topmemas.top/?mem=1770822180",
    "tags": ["salary", "taxes", "life"],
    "info": {
        "colors": ["green", "black", "white"],
        "objects": ["big dog", "small dog"]
    }
}


@pytest.fixture
def new_meme():
    return NEW_MEME_DATA.copy()

@pytest.fixture
def created_meme(create_meme, delete_meme, token, new_meme):
    create_meme.create_meme(new_meme, token)
    create_meme.check_status_is_ok()
    meme_id = create_meme.get_id()


    yield meme_id, new_meme


    delete_meme.delete_meme_by_id(meme_id, token)


@pytest.fixture
def created_meme_no_cleanup(create_meme, token):
    meme_data = {
        "text": "Meme for deletion test",
        "url": "http://example.com/delete.jpg",
        "tags": ["delete", "test"],
        "info": {"objects": ["test"], "colors": ["blue"]}
    }

    create_meme.create_meme(meme_data, token)
    create_meme.check_status_is_ok()
    meme_id = create_meme.get_id()

    yield meme_id, meme_data


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
def create_meme():
    return CreateMeme()

@pytest.fixture()
def token():
    auth = Authorize()
    auth.authorize_user("saule").check_status_is_ok()
    token_value = auth.get_token()
    assert token_value is not None, "Токен не получен"
    return token_value