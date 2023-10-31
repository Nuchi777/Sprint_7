import pytest
import requests

from register_new_courier import register_new_courier_and_return_login_password

url = 'http://qa-scooter.praktikum-services.ru'


@pytest.fixture
def courier():
    data = register_new_courier_and_return_login_password()
    yield data
    # логинимся под созданным курьером
    endpoint_login_courier = '/api/v1/courier/login'
    data_login = {
        "login": data[0],
        "password": data[1]
    }
    response = requests.post(f'{url}{endpoint_login_courier}', data=data_login)
    id_courier = response.json()['id']

    # удаляем созданного курьера
    endpoint_delete_courier = f'/api/v1/courier/{id_courier}'
    requests.delete(f'{url}{endpoint_delete_courier}')
