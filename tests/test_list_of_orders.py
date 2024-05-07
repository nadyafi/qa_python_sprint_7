import allure
import requests

from data import URL


@allure.suite('Список заказов')
class TestListOfOrders:
    @allure.title('Проверка списка заказов')
    @allure.description('Тест успешного возврата списка заказов в тело ответа')
    def test_oder_list(self):
        response = requests.get(URL.ORDER)
        assert response.status_code == 200 and 'orders' in response.json()
        assert type(response.json()['orders']) is list
