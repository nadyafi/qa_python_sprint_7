import requests
from data import URL
import base_page
import pytest
import allure

@allure.suite('Создание курьера')
class TestCreateCourier:

    @allure.title('Проверка успешного создания курьера')
    @allure.description('Тест создания курьера')
    def test_create_courier(self, unregistered_courier):
        payload = unregistered_courier
        response = requests.post(URL.COURIER, data=payload)
        assert response.status_code == 201 and response.text == '{"ok":true}'

    @allure.title('Проверка ошибки при создании одинаковых курьеров')
    @allure.description('Тест ошибки создания одинаковых курьеров')
    def test_create_same_courier(self, unregistered_courier):
        payload = unregistered_courier
        requests.post(URL.COURIER, data=payload)
        response_1 = requests.post(URL.COURIER, data=payload)
        assert response_1.status_code == 409 and response_1.json().get('message') \
               == "Этот логин уже используется. Попробуйте другой."

    @allure.title('Проверка обязательных полей при создании курьера')
    @allure.description('Тест при отсутствии обязательных полей при создании курьера')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_required_fields(self, missing_field):
        login, password, first_name = base_page.generate_unregistered_courier()
        payload = {
            'login': login,
            'password': password,
            'firstName': first_name
        }
        del payload[missing_field]
        response = requests.post(URL.COURIER, data=payload)
        assert response.status_code == 400 and response.json().get('message') == "Недостаточно данных для создания учетной записи"
