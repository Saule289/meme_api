from conftest import change_meme

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


def test_update_meme(create_meme, delete_meme, token):
    meme = new_meme
    change_meme().update_meme(meme, token)
    update_meme.check_status_is_ok()
    update_meme.check_text_is_correct()
    update_meme.check_info_is_correct()
    update_meme.check_tags_are_correct()
    meme_id = create_meme.get_id()
    delete_meme.delete_meme_by_id(meme_id, token)
    delete_meme.check_status_is_ok()