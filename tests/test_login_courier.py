import allure
import requests
import random
from data import Urls
from data import Endpoints


class TestLoginCourier:
    @allure.title('Авторизация в приложении пройдет успешно, если валидными данными заполнены все обязательные поля')
    def test_login_couriers(self, new_courier_return_login_password):
        data = new_courier_return_login_password
        login = data[0]
        password = data[1]

        data_login = {
            "login": login,
            "password": password
        }
        response = requests.post(f'{Urls.URL_SCOOTER}{Endpoints.LOGIN_COURIER}', data=data_login)
        id_courier = response.json()['id']
        assert response.status_code == 200 and response.text == f'{{"id":{id_courier}}}'

    @allure.title('Авторизация в приложении пройдет неуспешно, если обязательное поле login пустое')
    def test_login_couriers_required_field_login_empty(self, new_courier_return_login_password):
        data = new_courier_return_login_password
        password = data[1]

        data_login = {
            "login": "",
            "password": password
        }
        response = requests.post(f'{Urls.URL_SCOOTER}{Endpoints.LOGIN_COURIER}', data=data_login)
        assert response.status_code == 400 and response.text == '{"message":  "Недостаточно данных для входа"}'

    @allure.title('Авторизация в приложении пройдет неуспешно, если обязательное поле password пустое')
    def test_login_couriers_required_field_password_empty(self, new_courier_return_login_password):
        data = new_courier_return_login_password
        login = data[0]

        data_login = {
            "login": login,
            "password": ""
        }
        response = requests.post(f'{Urls.URL_SCOOTER}{Endpoints.LOGIN_COURIER}', data=data_login)
        assert response.status_code == 400 and response.text == '{"message":  "Недостаточно данных для входа"}'

    @allure.title('Авторизация в приложении пройдет неуспешно, если обязательное поле login заполнено не верно')
    def test_login_couriers_field_login_incorrect(self, new_courier_return_login_password):
        data = new_courier_return_login_password
        password = data[1]

        data_login = {
            "login": 'qwerty',
            "password": password
        }
        response = requests.post(f'{Urls.URL_SCOOTER}{Endpoints.LOGIN_COURIER}', data=data_login)
        assert response.status_code == 404 and response.text == '{"message":  "Учетная запись не найдена"}'

    @allure.title('Авторизация в приложении пройдет неуспешно, если обязательное поле password заполнено не верно')
    def test_login_couriers_field_password_incorrect(self, new_courier_return_login_password):
        data = new_courier_return_login_password
        login = data[0]

        data_login = {
            "login": login,
            "password": "12345"
        }
        response = requests.post(f'{Urls.URL_SCOOTER}{Endpoints.LOGIN_COURIER}', data=data_login)
        assert response.status_code == 404 and response.text == '{"message":  "Учетная запись не найдена"}'

    @allure.title('Авторизация в приложении пройдет неуспешно, если обязательное поле login не передано')
    def test_login_couriers_required_field_login_not_sending(self, new_courier_return_login_password):
        data = new_courier_return_login_password
        password = data[1]

        data_login = {
            "password": password
        }
        response = requests.post(f'{Urls.URL_SCOOTER}{Endpoints.LOGIN_COURIER}', data=data_login)
        assert response.status_code == 400 and response.text == '{"message":  "Недостаточно данных для входа"}'

    @allure.title('Авторизация в приложении пройдет неуспешно, если обязательное поле password не передано')
    def test_login_couriers_required_field_password_not_sending(self, new_courier_return_login_password):
        data = new_courier_return_login_password
        login = data[0]

        data_login = {
            "login": login
        }
        response = requests.post(f'{Urls.URL_SCOOTER}{Endpoints.LOGIN_COURIER}', data=data_login)
        assert response.status_code == 400 and response.text == '{"message":  "Недостаточно данных для входа"}'

    @allure.title('Авторизация в приложении пройдет неуспешно, если авторизоваться под несуществующим пользователем')
    def test_login_couriers_non_existent_user(self, new_courier_return_login_password):
        data = new_courier_return_login_password
        login = data[0]
        password = data[1]

        data_login = {
            "login": f"{login}{random.randint(100, 999)}",
            "password": f"{password}{random.randint(100, 999)}"
        }
        response = requests.post(f'{Urls.URL_SCOOTER}{Endpoints.LOGIN_COURIER}', data=data_login)
        assert response.status_code == 404 and response.text == '{"message":  "Учетная запись не найдена"}'

    @allure.title('Успешный запрос возвращает id пользователя в теле ответа')
    def test_login_couriers_return_id(self, new_courier_return_login_password):
        data = new_courier_return_login_password
        login = data[0]
        password = data[1]

        data_login = {
            "login": login,
            "password": password
        }
        response = requests.post(f'{Urls.URL_SCOOTER}{Endpoints.LOGIN_COURIER}', data=data_login)
        id_courier = response.json()['id']
        assert response.status_code == 200 and response.text == f'{{"id":{id_courier}}}'


