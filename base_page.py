import requests
import random
import string
from data import URL


def register_new_courier_and_return_login_password():
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # создаём список, чтобы метод мог его вернуть
    login_pass = []

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post(URL.COURIER, data=payload)

    # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    # возвращаем список
    return login_pass


def generate_unregistered_courier():
    def generate_string(length):
        random_string = ''.join(random.choices(string.ascii_lowercase, k=length))
        return random_string

    courier_data = []
    while len(courier_data) != 3:
        courier_data.append(generate_string(8))
    return courier_data


def new_courier():
    login, password, first_name = register_new_courier_and_return_login_password()
    courier = {
        'login': login,
        'password': password
    }
    return courier


def non_existing_courier():
    response = requests.post(URL.LOGIN, data=new_courier())
    courier_id = response.json()["id"] + random.randint(1, 999)
    return courier_id
