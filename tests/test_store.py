import allure
import pytest
import requests
import jsonschema

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:

    @allure.title("Размещение заказа (POST /store/order)")
    def test_add_new_order(self):
        with allure.step("Подготовка данных для размещения заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на создание нового заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, f"Ожидаю код 200, а получил {response.status_code}"

        with allure.step("Проверка параметров заказа в ответе"):
            assert response_json['id'] == payload['id'], f"id заказа не совпадает с ожидаемым"
            assert response_json['petId'] == payload['petId'], f"PetId не совпадает с ожидаемым"
            assert response_json['quantity'] == payload['quantity'], f"quantity не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], f"status не совпадает с ожидаемым"
            assert response_json['complete'] == payload['complete'], f"complete не совпадает с ожидаемым"

