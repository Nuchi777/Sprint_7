import json
import requests

from register_new_courier import register_new_courier_and_return_login_password

url = 'http://qa-scooter.praktikum-services.ru'


class TestCreateCourier:
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

    def test_cannot_create_two_identical_couriers(self):

        # создаем курьера
        data = register_new_courier_and_return_login_password()
        login = data[0]
        password = data[1]
        firstName = data[2]

        # логинимся под созданным курьером
        endpoint_login_courier = '/api/v1/courier/login'
        data_login = {
            "login": f"{login}",
            "password": f"{password}"
        }
        response = requests.post(f'{url}{endpoint_login_courier}', data=data_login)
        id_courier = response.json()['id']
        assert response.status_code == 200

        # создаем курьера с теми же параметрами
        endpoint_create_courier = '/api/v1/courier'
        data_create = {
            "login": f"{login}",
            "password": f"{password}",
            "firstName": f"{firstName}"
        }
        response = requests.post(f'{url}{endpoint_create_courier}', data=data_create)
        assert response.status_code == 409 and response.text == '{"message": "Этот логин уже используется"}'

        # удаляем созданного курьера
        endpoint_delete_courier = f'/api/v1/courier/{id_courier}'
        response = requests.delete(f'{url}{endpoint_delete_courier}')
        assert response.status_code == 200





class TestLoginCourier:
    pass


class TestCreateOrder:
    pass


class TestListOrders:
    pass
