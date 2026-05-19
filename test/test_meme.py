
def test_create_meme(create_meme, delete_meme, token, new_meme):
    create_meme.create_meme(new_meme, token)  # Используем фикстуру
    create_meme.check_status_is_ok()
    meme_id = create_meme.get_id()


    assert create_meme.json['text'] == new_meme['text']
    assert create_meme.json['url'] == new_meme['url']
    assert create_meme.json['tags'] == new_meme['tags']
    assert create_meme.json['info'] == new_meme['info']

    delete_meme.delete_meme_by_id(meme_id, token)


def test_get_meme(created_meme, get_meme_by_id, token):
    meme_id, meme_data = created_meme

    get_meme_by_id.get_meme_by_id(meme_id, token)
    get_meme_by_id.check_status_is_ok()

    assert get_meme_by_id.json['text'] == meme_data['text']
    assert get_meme_by_id.json['url'] == meme_data['url']
    assert get_meme_by_id.json['tags'] == meme_data['tags']
    assert get_meme_by_id.json['info'] == meme_data['info']


def test_update_meme(create_meme, change_meme, delete_meme, token, new_meme):
    meme = new_meme
    create_meme.create_meme(meme, token)
    create_meme.check_status_is_ok()
    updated_meme_id = create_meme.get_id()


    updated_meme = meme.copy()
    updated_meme["text"] = "Updated meme text"
    updated_meme["tags"].append("salary")


    change_meme.update_meme(
        meme_id=updated_meme_id,
        text=updated_meme["text"],
        url=updated_meme["url"],
        tags=updated_meme["tags"],
        info=updated_meme["info"],
        token=token
    )
    change_meme.check_status_is_ok()


    assert change_meme.json is not None, "Response JSON is None"
    assert change_meme.json['text'] == "Updated meme text", "Text not updated"
    assert change_meme.json['url'] == updated_meme['url'], "URL changed unexpectedly"
    assert "salary" in change_meme.json['tags'], "Tag 'salary' not added"
    assert change_meme.json['info'] == updated_meme['info'], "Info changed unexpectedly"
    assert int(change_meme.json['id']) == updated_meme_id, "Meme ID changed"

    delete_meme.delete_meme_by_id(updated_meme_id, token)
    delete_meme.check_status_is_ok()


def test_delete_meme(create_meme, get_meme_by_id, delete_meme, token):
    meme = new_meme
    create_meme.create_meme(meme, token)
    meme_id = create_meme.get_id()
    get_meme_by_id.get_meme_by_id(meme_id, token)
    delete_meme.delete_meme_by_id(meme_id, token)
    delete_meme.check_status_is_ok()
    get_meme_by_id.get_meme_by_id(meme_id, token)
    get_meme_by_id.check_status_not_found()


def test_create_meme_without_token(create_meme):
    meme = new_meme
    create_meme.create_meme(meme, token=None)
    create_meme.check_that_user_is_unauthorized()


def test_create_meme_with_invalid_token(create_meme):
    meme = new_meme
    create_meme.create_meme(meme, token="0000000")
    create_meme.check_that_user_is_unauthorized()


def test_get_meme_with_wrong_id(get_meme_by_id, token):
    wrong_id = "1234567890"
    get_meme_by_id.get_meme_by_id(wrong_id, token)
    get_meme_by_id.check_status_not_found()


def test_create_meme_with_invalid_payload(create_meme, token):
    meme = {
        "text": None,
        "url": "not_a_url",
        "tags": "wrong_format",
        "info": {}
    }

    create_meme.create_meme(meme, token)
    create_meme.check_that_status_is_bad_request()



def test_delete_already_deleted_meme(create_meme, delete_meme, token):
    meme = new_meme

    create_meme.create_meme(meme, token)
    meme_id = create_meme.get_id()

    delete_meme.delete_meme_by_id(meme_id, token)
    delete_meme.check_status_is_ok()

    delete_meme.delete_meme_by_id(meme_id, token)
    delete_meme.check_status_not_found()
