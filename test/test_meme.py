import allure

new_meme = {
"text": "Why this is so",
"url": "https://topmemas.top/?mem=1770822180",
"tags": ["salary","taxes", "life"],
"info": {
        "colors": [
            "green",
            "black",
            "white"
        ],
        "objects": [
            "big dog",
            "small dog"
        ]
}
}


def test_create_meme(create_meme, delete_meme, token):
    meme = new_meme
    create_meme.create_meme(meme, token)
    create_meme.check_status_is_ok()
    create_meme.check_text_is_correct()
    create_meme.check_info_is_correct()
    create_meme.check_tags_are_correct()
    meme_id = create_meme.get_id()
    delete_meme.delete_meme_by_id(meme_id, token)
    delete_meme.check_status_is_ok()


def test_get_meme(create_meme, get_meme_by_id, delete_meme, token):
    meme = new_meme
    create_meme.create_meme(meme, token)
    meme_id = create_meme.get_id()
    get_meme_by_id.get_meme_by_id(meme_id, token)
    get_meme_by_id.check_status_is_ok()
    get_meme_by_id.check_text_is_correct()
    get_meme_by_id.check_info_is_correct()
    get_meme_by_id.check_tags_are_correct()
    delete_meme.delete_meme_by_id(meme_id, token)


def test_update_meme(create_meme, change_meme, delete_meme, token):
    meme = new_meme
    create_meme.create_meme(meme, token)
    create_meme.check_status_is_ok()
    updated_meme_id = create_meme.get_id()
    updated_meme = meme.copy()
    updated_meme["text"] = "Updated meme text"
    updated_meme["tags"].append("salary")
    change_meme.update_meme(
        meme_id = updated_meme_id,
        text = updated_meme["text"],
        info = updated_meme["info"],
        tags = updated_meme["tags"],
        url = updated_meme["url"],
        token = token
    )
    change_meme.check_status_is_ok()
    change_meme.check_text_is_correct()
    change_meme.check_info_is_correct()
    change_meme.check_tags_are_correct()
    change_meme.check_meme_id_is_correct()
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
