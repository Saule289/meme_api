import allure
import pytest


@allure.feature('Meme API Tests')
class TestMemeAPI:

    @allure.story('Create Meme')
    @allure.title('Создание нового мема')
    def test_create_meme(self, create_meme, token, new_meme):
        with allure.step("Подготовка данных для создания мема"):
            allure.attach(str(new_meme), "Данные мема", allure.attachment_type.JSON)

        with allure.step("Отправка запроса на создание мема"):
            create_meme.create_meme(new_meme, token)

        with allure.step("Проверка статуса ответа"):
            create_meme.check_status_is_ok()

        with allure.step("Получение ID созданного мема"):
            meme_id = create_meme.get_id()
            allure.attach(str(meme_id), "ID созданного мема", allure.attachment_type.TEXT)

        with allure.step("Проверка полей созданного мема"):
            assert create_meme.json['text'] == new_meme['text'], "Текст не совпадает"
            assert create_meme.json['url'] == new_meme['url'], "URL не совпадает"
            assert create_meme.json['tags'] == new_meme['tags'], "Теги не совпадают"
            assert create_meme.json['info'] == new_meme['info'], "Info не совпадает"

        with allure.step(f"Очистка: удаление мема {meme_id}"):
            from endpoints.delete_meme import DeleteMeme
            delete_meme = DeleteMeme()
            delete_meme.delete_meme_by_id(meme_id, token)

    @allure.story('Get Meme')
    @allure.title('Получение мема по ID')
    def test_get_meme(self, created_meme, get_meme_by_id, token):
        meme_id, meme_data = created_meme

        with allure.step(f"Получение мема с ID {meme_id}"):
            allure.attach(str(meme_id), "ID мема", allure.attachment_type.TEXT)
            get_meme_by_id.get_meme_by_id(meme_id, token)

        with allure.step("Проверка статуса ответа"):
            get_meme_by_id.check_status_is_ok()

        with allure.step("Проверка полей полученного мема"):
            assert get_meme_by_id.json['text'] == meme_data['text'], "Текст не совпадает"
            assert get_meme_by_id.json['url'] == meme_data['url'], "URL не совпадает"
            assert get_meme_by_id.json['tags'] == meme_data['tags'], "Теги не совпадают"
            assert get_meme_by_id.json['info'] == meme_data['info'], "Info не совпадает"


    @allure.story('Update Meme')
    @allure.title('Обновление существующего мема')
    def test_update_meme(self, created_meme, change_meme, token):
        meme_id, original_meme = created_meme

        with allure.step(f"Подготовка данных для обновления мема {meme_id}"):
            updated_meme = original_meme.copy()
            updated_meme["text"] = "Updated meme text"
            updated_meme["tags"].append("salary")
            allure.attach(str(updated_meme), "Обновленные данные", allure.attachment_type.JSON)

        with allure.step("Отправка запроса на обновление мема"):
            change_meme.update_meme(
                meme_id=meme_id,
                text=updated_meme["text"],
                url=updated_meme["url"],
                tags=updated_meme["tags"],
                info=updated_meme["info"],
                token=token
            )

        with allure.step("Проверка статуса ответа"):
            change_meme.check_status_is_ok()

        with allure.step("Проверка обновленных полей"):
            assert change_meme.json['text'] == "Updated meme text", "Текст не обновился"
            assert "salary" in change_meme.json['tags'], "Тег 'salary' не добавлен"
            assert int(change_meme.json['id']) == meme_id, "ID мема изменился"

    @allure.story('Delete Meme')
    @allure.title('Удаление существующего мема')
    def test_delete_meme(self, created_meme_no_cleanup, get_meme_by_id, delete_meme, token):
        meme_id, meme_data = created_meme_no_cleanup

        with allure.step(f"Проверка что мем {meme_id} существует"):
            get_meme_by_id.get_meme_by_id(meme_id, token)
            get_meme_by_id.check_status_is_ok()
            allure.attach(str(meme_id), "ID мема для удаления", allure.attachment_type.TEXT)

        with allure.step(f"Удаление мема {meme_id}"):
            delete_meme.delete_meme_by_id(meme_id, token)

        with allure.step("Проверка успешного удаления"):
            delete_meme.check_status_is_ok()

        with allure.step(f"Проверка что мем {meme_id} больше не существует"):
            get_meme_by_id.get_meme_by_id(meme_id, token)
            get_meme_by_id.check_status_not_found()
            allure.attach("Мем успешно удален", "Результат", allure.attachment_type.TEXT)


@allure.feature('Negative Tests')
class TestNegativeMemeAPI:

    @allure.story('Authentication - No Token')
    @allure.title('Создание мема без токена')
    def test_create_meme_without_token(self, create_meme, new_meme):
        with allure.step("Попытка создания мема без токена"):
            create_meme.create_meme(new_meme, token=None)

        with allure.step("Проверка что запрос отклонен (401 Unauthorized)"):
            create_meme.check_that_user_is_unauthorized()
            allure.attach("Запрос без токена корректно отклонен", "Результат", allure.attachment_type.TEXT)

    @allure.story('Authentication - Invalid Token')
    @allure.title('Создание мема с невалидным токеном')
    @pytest.mark.parametrize("invalid_token", [None, "", "0000000", "invalid", "Bearer xyz"])
    def test_create_meme_with_invalid_token(self, create_meme, new_meme, invalid_token):
        with allure.step(f"Попытка создания мема с токеном: '{invalid_token}'"):
            create_meme.create_meme(new_meme, token=invalid_token)

        with allure.step("Проверка что запрос отклонен (401 Unauthorized)"):
            create_meme.check_that_user_is_unauthorized()
            allure.attach(f"Токен '{invalid_token}' корректно отклонен", "Результат", allure.attachment_type.TEXT)

    @allure.story('Create Meme - Known API Issues')
    @allure.title('Создание мема с невалидными данными (документирование багов API)')
    @pytest.mark.parametrize("invalid_meme, reason", [
        ({"text": "", "url": "http://ok.com", "tags": ["ok"], "info": {}}, "API allows empty text"),
        ({"text": "ok", "url": "not_a_url", "tags": ["ok"], "info": {}}, "API doesn't validate URL"),
    ])
    @pytest.mark.xfail(reason="API bug: should validate these fields", strict=False)
    def test_create_meme_validation_bugs(self, create_meme, token, invalid_meme, reason):
        with allure.step(f"Попытка создания мема с невалидными данными: {reason}"):
            allure.attach(str(invalid_meme), "Невалидные данные", allure.attachment_type.JSON)
            create_meme.create_meme(invalid_meme, token)

        with allure.step("Проверка что API должен вернуть ошибку (ожидается 400/422)"):
            assert create_meme.response.status_code in [400, 422], \
                f"Should validate: {reason}"
            allure.attach(f"API вернул {create_meme.response.status_code}", "Статус ответа",
                          allure.attachment_type.TEXT)

    @allure.story('Get Meme - Invalid ID')
    @allure.title('Получение мема по несуществующему ID')
    @pytest.mark.parametrize("wrong_id", ["1234567890", 999999999, "invalid", "", None])
    def test_get_meme_with_wrong_id(self, get_meme_by_id, token, wrong_id):
        with allure.step(f"Попытка получения мема с ID: {wrong_id}"):
            allure.attach(str(wrong_id), "Невалидный ID", allure.attachment_type.TEXT)
            get_meme_by_id.get_meme_by_id(wrong_id, token)

        with allure.step("Проверка что возвращен статус 404 Not Found"):
            get_meme_by_id.check_status_not_found()


    @allure.story('Update Meme - Invalid Data')
    @allure.title('Обновление мема с невалидными данными')
    @pytest.mark.parametrize("field, bad_value", [
        ("tags", "not_a_list"),
        ("info", "not_a_dict"),
    ])
    def test_update_meme_invalid_data(self, created_meme, change_meme, token, field, bad_value):
        meme_id, original_meme = created_meme

        with allure.step(f"Подготовка данных: поле '{field}' = '{bad_value}'"):
            invalid_data = original_meme.copy()
            invalid_data[field] = bad_value
            allure.attach(str(invalid_data), "Невалидные данные", allure.attachment_type.JSON)

        with allure.step(f"Отправка запроса на обновление мема {meme_id} с невалидным полем '{field}'"):
            change_meme.update_meme(
                meme_id=meme_id,
                text=invalid_data["text"],
                url=invalid_data["url"],
                tags=invalid_data["tags"],
                info=invalid_data["info"],
                token=token
            )

        with allure.step("Проверка что API вернул ошибку (400/422)"):
            assert change_meme.response.status_code in [400, 422], \
                f"Expected 400/422, got {change_meme.response.status_code}"

    @allure.story('Update Meme - Known API Issues')
    @allure.title('Обновление мема с пустым текстом (документирование бага API)')
    @pytest.mark.xfail(reason="API bug: allows empty text", strict=True)
    def test_update_meme_empty_text(self, created_meme, change_meme, token):
        meme_id, original_meme = created_meme

        with allure.step("Попытка обновить мем с пустым текстом"):
            change_meme.update_meme(
                meme_id=meme_id,
                text="",
                url=original_meme["url"],
                tags=original_meme["tags"],
                info=original_meme["info"],
                token=token
            )

        with allure.step("Проверка что API вернул ошибку (ожидается 400/422)"):
            assert change_meme.response.status_code in [400, 422], \
                f"Expected 400/422, got {change_meme.response.status_code}"


    @allure.story('Delete Meme - Invalid ID')
    @allure.title('Удаление несуществующего мема')
    @pytest.mark.parametrize("wrong_id", [
        None,
        "",
        "invalid_id",
        999999999,
    ])
    def test_delete_nonexistent_meme(self, delete_meme, token, wrong_id):
        with allure.step(f"Попытка удаления мема с ID: {wrong_id}"):
            allure.attach(str(wrong_id), "Невалидный ID", allure.attachment_type.TEXT)
            delete_meme.delete_meme_by_id(wrong_id, token)

        with allure.step("Проверка что возвращен статус 404 Not Found"):
            delete_meme.check_status_not_found()
