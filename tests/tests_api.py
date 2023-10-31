import json
import allure
import pytest
import requests
import random


url = 'http://qa-scooter.praktikum-services.ru'


class TestCreateCourier:
    @allure.title('Регистрация в приложении пройдет успешно, если валидными данными заполнены все поля')
    def test_can_create_courier(self):
        # создаем курьера
        endpoint_create_courier = '/api/v1/courier'
        data_create = {
            "login": "e.koloskov",
            "password": "12345",
            "firstName": "Evgeny"
        }
        response = requests.post(f'{url}{endpoint_create_courier}', data=data_create)
        assert response.status_code == 201 and response.text == '{"ok":true}'

        # логинимся под созданным курьером
        endpoint_login_courier = '/api/v1/courier/login'
        data_login = {
            "login": "e.koloskov",
            "password": "12345"
        }
        response = requests.post(f'{url}{endpoint_login_courier}', data=data_login)
        id_courier = response.json()['id']
        assert response.status_code == 200

        # удаляем созданного курьера
        endpoint_delete_courier = f'/api/v1/courier/{id_courier}'
        response = requests.delete(f'{url}{endpoint_delete_courier}')
        assert response.status_code == 200

    @allure.title('Регистрация в приложении пройдет неуспешно, если повторно создать пользователя с теми же параметрами')
    def test_cannot_create_two_identical_couriers(self, courier):
        # создаем курьера
        data = courier
        login = data[0]
        password = data[1]
        firstName = data[2]

        # создаем курьера с теми же параметрами
        endpoint_create_courier = '/api/v1/courier'
        data_create = {
            "login": login,
            "password": password,
            "firstName": firstName
        }
        response = requests.post(f'{url}{endpoint_create_courier}', data=data_create)
        assert response.status_code == 409 and response.text == '{"message": "Этот логин уже используется"}'

    @allure.title('Регистрация в приложении пройдет неуспешно, если поле login или password пустое')
    @pytest.mark.parametrize("login, password", [["", "12345"], ["e.koloskov", ""]])
    def test_create_couriers_fill_not_all_required_field(self, login, password):
        # создаем курьера без логина или пароля
        endpoint_create_courier = '/api/v1/courier'
        data_create = {
            "login": login,
            "password": password
        }
        response = requests.post(f'{url}{endpoint_create_courier}', data=data_create)
        assert response.status_code == 400 and response.text == '{"message": "Недостаточно данных для создания учетной записи"}'

    @allure.title('Регистрация в приложении пройдет неуспешно, если поле login или password не передано')
    @pytest.mark.parametrize("data_create", [{"password": "12345"}, {"login": "e.koloskov"}])
    def test_create_couriers_required_field_login_or_password_not_sending(self, data_create):
        # создаем курьера. Не передаем логин или пароль
        endpoint_create_courier = '/api/v1/courier'
        response = requests.post(f'{url}{endpoint_create_courier}', data=data_create)
        assert response.status_code == 400 and response.text == '{"message": "Недостаточно данных для создания учетной записи"}'

    @allure.title('Регистрация в приложении пройдет неуспешно, если поле login дублирует ранее созданную в БД запись')
    def test_create_couriers_with_login_in_database(self, courier):
        # создаем курьера
        data = courier
        login = data[0]

        # создаем курьера с тем же логином
        endpoint_create_courier = '/api/v1/courier'
        data_create = {
            "login": login,
            "password": "12345"
        }
        response = requests.post(f'{url}{endpoint_create_courier}', data=data_create)
        assert response.status_code == 409 and response.text == '{"message": "Этот логин уже используется"}'


class TestLoginCourier:
    @allure.title('Авторизация в приложении пройдет успешно, если валидными данными заполнены все обязательные поля')
    def test_login_couriers(self, courier):
        # создаем курьера
        data = courier
        login = data[0]
        password = data[1]

        # логинимся под созданным курьером
        endpoint_login_courier = '/api/v1/courier/login'
        data_login = {
            "login": login,
            "password": password
        }
        response = requests.post(f'{url}{endpoint_login_courier}', data=data_login)
        id_courier = response.json()['id']
        assert response.status_code == 200 and response.text == f'{{"id":{id_courier}}}'

    @allure.title('Авторизация в приложении пройдет неуспешно, если обязательное поле login пустое')
    def test_login_couriers_required_field_login_empty(self, courier):
        # создаем курьера
        data = courier
        password = data[1]

        # логинимся под созданным курьером без логина
        endpoint_login_courier = '/api/v1/courier/login'
        data_login = {
            "login": "",
            "password": password
        }
        response = requests.post(f'{url}{endpoint_login_courier}', data=data_login)
        assert response.status_code == 400 and response.text == '{"message":  "Недостаточно данных для входа"}'

    @allure.title('Авторизация в приложении пройдет неуспешно, если обязательное поле password пустое')
    def test_login_couriers_required_field_password_empty(self, courier):
        # создаем курьера
        data = courier
        login = data[0]

        # логинимся под созданным курьером без пароля
        endpoint_login_courier = '/api/v1/courier/login'
        data_login = {
            "login": login,
            "password": ""
        }
        response = requests.post(f'{url}{endpoint_login_courier}', data=data_login)
        assert response.status_code == 400 and response.text == '{"message":  "Недостаточно данных для входа"}'

    @allure.title('Авторизация в приложении пройдет неуспешно, если обязательное поле login заполнено не верно')
    def test_login_couriers_field_login_incorrect(self, courier):
        # создаем курьера
        data = courier
        password = data[1]

        # логинимся под созданным курьером c неправильным логином
        endpoint_login_courier = '/api/v1/courier/login'
        data_login = {
            "login": 'qwerty',
            "password": password
        }
        response = requests.post(f'{url}{endpoint_login_courier}', data=data_login)
        assert response.status_code == 404 and response.text == '{"message":  "Учетная запись не найдена"}'

    @allure.title('Авторизация в приложении пройдет неуспешно, если обязательное поле password заполнено не верно')
    def test_login_couriers_field_password_incorrect(self, courier):
        # создаем курьера
        data = courier
        login = data[0]

        # логинимся под созданным курьером c неправильным паролем
        endpoint_login_courier = '/api/v1/courier/login'
        data_login = {
            "login": login,
            "password": "12345"
        }
        response = requests.post(f'{url}{endpoint_login_courier}', data=data_login)
        assert response.status_code == 404 and response.text == '{"message":  "Учетная запись не найдена"}'

    @allure.title('Авторизация в приложении пройдет неуспешно, если обязательное поле login не передано')
    def test_login_couriers_required_field_login_not_sending(self, courier):
        # создаем курьера
        data = courier
        password = data[1]

        # логинимся под созданным курьером без логина
        endpoint_login_courier = '/api/v1/courier/login'
        data_login = {
            "password": password
        }
        response = requests.post(f'{url}{endpoint_login_courier}', data=data_login)
        assert response.status_code == 400 and response.text == '{"message":  "Недостаточно данных для входа"}'

    @allure.title('Авторизация в приложении пройдет неуспешно, если обязательное поле password не передано')
    def test_login_couriers_required_field_password_not_sending(self, courier):
        # создаем курьера
        data = courier
        login = data[0]

        # логинимся под созданным курьером без пароля
        endpoint_login_courier = '/api/v1/courier/login'
        data_login = {
            "login": login
        }
        response = requests.post(f'{url}{endpoint_login_courier}', data=data_login)
        assert response.status_code == 400 and response.text == '{"message":  "Недостаточно данных для входа"}'

    @allure.title('Авторизация в приложении пройдет неуспешно, если авторизоваться под несуществующим пользователем')
    def test_login_couriers_non_existent_user(self, courier):
        # создаем курьера
        data = courier
        login = data[0]
        password = data[1]
        # логинимся под несуществующим курьером
        endpoint_login_courier = '/api/v1/courier/login'
        data_login = {
            "login": f"{login}{random.randint(100, 999)}",
            "password": f"{password}{random.randint(100, 999)}"
        }
        response = requests.post(f'{url}{endpoint_login_courier}', data=data_login)
        assert response.status_code == 404 and response.text == '{"message":  "Учетная запись не найдена"}'

    @allure.title('Успешный запрос возвращает id пользователя в теле ответа')
    def test_login_couriers_return_id(self, courier):
        # создаем курьера
        data = courier
        login = data[0]
        password = data[1]
        # логинимся под созданным курьером
        endpoint_login_courier = '/api/v1/courier/login'
        data_login = {
            "login": login,
            "password": password
        }
        response = requests.post(f'{url}{endpoint_login_courier}', data=data_login)
        id_courier = response.json()['id']
        assert response.status_code == 200 and response.text == f'{{"id":{id_courier}}}'


class TestCreateOrder:
    @allure.title('При оформлении заказа можно указать один из цветов самоката')
    @pytest.mark.parametrize("color", ['BLACK', 'GREY', "BLACK, GREY", ''])
    def test_create_order_can_choose_scooter_colors_black_or_grey(self, color):
        # создаем заказ
        endpoint_create_order = '/api/v1/orders'
        data_create_order = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": [color]
        }
        data_create_order_json = json.dumps(data_create_order)
        response = requests.post(f'{url}{endpoint_create_order}', data=data_create_order_json)
        track_order = response.json()['track']
        assert response.status_code == 201 and response.text == f'{{"track":{track_order}}}'



class TestListOrders:
    @allure.title('При получении списка заказов в тело ответа возвращается список заказов')
    def test_return_list_orders_in_body(self):
        endpoint_login_courier = '/api/v1/orders'
        response = requests.get(f'{url}{endpoint_login_courier}')
        list_orders = response.json()['orders']
        assert response.status_code == 200 and len(list_orders) != 0
