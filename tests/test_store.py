import allure
import pytest
import requests
import jsonschema

from tests.conftest import create_pet

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


    @allure.title("Получение информации о заказе по ID (GET /store/order/{orderId})")
    def test_get_order_by_id(self, create_order):
        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(url=f"{BASE_URL}/store/order/1")
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, f"Ожидаю код 200, а получил {response.status_code}"

        with allure.step("Проверка параметров заказа в ответе"):
            assert response_json['id'] == create_order['id'], f"id заказа не совпадает с ожидаемым"
            assert response_json['petId'] == create_order['petId'], f"petId заказа не совпадает с ожидаемым"
            assert response_json['quantity'] == create_order['quantity'], f"quantity заказа не совпадает с ожидаемым"
            assert response_json['status'] == create_order['status'], f"status заказа не совпадает с ожидаемым"
            assert response_json['complete'] == create_order['complete'], f"complete заказа не совпадает с ожидаемым"


    @allure.title("Удаление заказа по ID (DELETE /store/order/{orderId})")
    def test_delete_order_by_id(self, create_order):
        with allure.step("Отправка запроса на удаление заказа по ID"):
            response = requests.delete(url=f"{BASE_URL}/store/order/1")
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(url=f"{BASE_URL}/store/order/1")
            assert response.status_code == 404, f"Ожидался статус 404, но получен {response.status_code}"
            assert "Order not found" in response.text, f" Ожидался текст 'Order not found', но получен '{response.text}'"


    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):
        with allure.step("Отправка запроса на получение несуществующего заказа"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, f"Ожидаю код 404, а получил {response.status_code}"

        with allure.step("Проверка текстового содержимого ответа"):
            assert "Order not found" in response.text, f" Ожидался текст 'Order not found', но получен '{response.text}'"


    @allure.title("Получение инвентаря магазина (GET /store/inventory)")
    def test_get_inventory(self):
        with allure.step("Отправка запроса на получение инвентаря магазина"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")
            assert response.status_code == 200
            assert isinstance(response.json(), dict)



