import requests
from data import URL, Answers
import helpers
import pytest
import allure


@allure.suite('Логин курьера в системе')
class TestLoginCourier:
    @allure.title('Проверка успешной авторизации курьера в системе')
    @allure.description('Тест успешной авторизации курьера в системе')
    def test_login_courier(self, registered_courier):
        payload = registered_courier
        response = requests.post(URL.LOGIN, data=payload)
        assert response.status_code == 200 and 'id' in response.text

    @allure.title('Проверка обязательных полей при авторизации')
    @allure.description('Тест авторизации при отсутствии обязательных полей')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_required_fields(self, registered_courier, missing_field):
        payload = registered_courier.copy()
        payload[missing_field] = ''
        response = requests.post(URL.LOGIN, data=payload)
        assert response.status_code == 400 and response.json().get('message') == Answers.LITTLE_DATA_FOR_AUTH

    @allure.title('Проверка некорректных данных при авторизации')
    @allure.description('Тест авторизации с некорректными данными')
    @pytest.mark.parametrize('invalid_field', ['login', 'password'])
    def test_login_courier_with_invalid_field(self, registered_courier, invalid_field):
        payload = registered_courier.copy()
        payload[invalid_field] += '1'
        response = requests.post(URL.LOGIN, data=payload)
        assert response.status_code == 404 and response.json().get('message') == Answers.ACCOUNT_NOT_FOUND

    @allure.title('Проверка авторизации незарегистрированного пользователя')
    @allure.description('Тест авторизации для незарегистрированного пользователя')
    def test_login_unregistered_courier(self):
        login, password, first_name = helpers.generate_unregistered_courier()
        payload = {
            'login': login,
            'password': password
        }
        response = requests.post(URL.LOGIN, data=payload)
        assert response.status_code == 404 and response.json().get('message') == Answers.ACCOUNT_NOT_FOUND
