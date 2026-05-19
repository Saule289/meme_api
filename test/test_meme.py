import pytest


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


def test_delete_meme(created_meme_no_cleanup, get_meme_by_id, delete_meme, token):
    meme_id, meme_data = created_meme_no_cleanup

    get_meme_by_id.get_meme_by_id(meme_id, token)
    get_meme_by_id.check_status_is_ok()


    delete_meme.delete_meme_by_id(meme_id, token)
    delete_meme.check_status_is_ok()

    get_meme_by_id.get_meme_by_id(meme_id, token)
    get_meme_by_id.check_status_not_found()


def test_create_meme_without_token(create_meme, new_meme):
    meme = new_meme
    create_meme.create_meme(meme, token=None)
    create_meme.check_that_user_is_unauthorized()


@pytest.mark.parametrize("invalid_token", [None, "", "0000000", "invalid", "Bearer xyz"])
def test_create_meme_with_invalid_token(create_meme, new_meme, invalid_token):
    create_meme.create_meme(new_meme, token=invalid_token)
    create_meme.check_that_user_is_unauthorized()


@pytest.mark.parametrize("wrong_id", ["1234567890", 999999999, "invalid", "", None])
def test_get_meme_with_wrong_id(get_meme_by_id, token, wrong_id):
    get_meme_by_id.get_meme_by_id(wrong_id, token)
    get_meme_by_id.check_status_not_found()

@pytest.mark.xfail(reason="API bug: allows empty text", strict=True)
@pytest.mark.parametrize("field, bad_value", [
    ("text", ""),
    ("tags", "not_a_list"),
    ("info", "not_a_dict"),
])
def test_update_meme_invalid_data(created_meme, change_meme, token, field, bad_value):


    invalid_data = original_meme.copy()
    invalid_data[field] = bad_value

    change_meme.update_meme(
        meme_id=meme_id,
        text=invalid_data["text"],
        url=invalid_data["url"],
        tags=invalid_data["tags"],
        info=invalid_data["info"],
        token=token
    )

    assert change_meme.response.status_code in [400, 422], \
        f"Expected 400/422, got {change_meme.response.status_code}"



@pytest.mark.parametrize("wrong_id", [
    None,
    "",
    "invalid_id",
    999999999,
])
def test_delete_nonexistent_meme(delete_meme, token, wrong_id):
    delete_meme.delete_meme_by_id(wrong_id, token)
    delete_meme.check_status_not_found()
