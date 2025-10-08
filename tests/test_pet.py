import allure
import requests

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:

    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, f"Ожидаю код ответа 200, а получили {response.status_code}"

        with allure.step("Проверка текстового содержимого ответа"):
            assert "Pet deleted" in response.text, f"Ожидаю, что текст Pet deleted есть в response, но его нет. response выглядит так {response.text}"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, f"Ожидаю код ответа 404, а получили {response.status_code}"

        with allure.step("Проверка текстового содержимого ответа"):
            assert "Pet not found" in response.text, f"Ожидаю, что текст Pet not found есть в response, но его нет. response выглядит так {response.text}"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение несуществующего питомца"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, f"Ожидаю код ответа 404, а получили {response.status_code}"

        with allure.step("Проверка текстового содержимого ответа"):
            assert "Pet not found" in response.text, f"Ожидаю, что текст Pet not found есть в response, но его нет. response выглядит так {response.text}"
