import allure
import pytest
import requests
from data import Urls
from data import Endpoints


class TestCreateCourier:
    @allure.title('Регистрация в приложении пройдет успешно, если валидными данными заполнены все поля')
    def test_can_create_courier(self, new_courier_return_response):
        response = new_courier_return_response
        assert response.status_code == 201 and response.text == '{"ok":true}'

    @allure.title(
        'Регистрация в приложении пройдет неуспешно, если повторно создать пользователя с теми же параметрами')
    def test_cannot_create_two_identical_couriers(self, new_courier_return_login_password):
        data = new_courier_return_login_password
        login = data[0]
        password = data[1]
        firstName = data[2]

        data_create = {
            "login": login,
            "password": password,
            "firstName": firstName
        }
        response = requests.post(f'{Urls.URL_SCOOTER}{Endpoints.CREATE_COURIER}', data=data_create)
        assert response.status_code == 409 and response.text == '{"message": "Этот логин уже используется"}'

    @allure.title('Регистрация в приложении пройдет неуспешно, если поле login или password пустое')
    @pytest.mark.parametrize("login, password", [["", "12345"], ["e.koloskov", ""]])
    def test_create_couriers_fill_not_all_required_field(self, login, password):
        data_create = {
            "login": login,
            "password": password
        }
        response = requests.post(f'{Urls.URL_SCOOTER}{Endpoints.CREATE_COURIER}', data=data_create)
        assert response.status_code == 400 and response.text == '{"message": "Недостаточно данных для создания учетной записи"}'

    @allure.title('Регистрация в приложении пройдет неуспешно, если поле login или password не передано')
    @pytest.mark.parametrize("data_create", [{"password": "12345"}, {"login": "e.koloskov"}])
    def test_create_couriers_required_field_login_or_password_not_sending(self, data_create):
        response = requests.post(f'{Urls.URL_SCOOTER}{Endpoints.CREATE_COURIER}', data=data_create)
        assert response.status_code == 400 and response.text == '{"message": "Недостаточно данных для создания учетной записи"}'

    @allure.title('Регистрация в приложении пройдет неуспешно, если поле login дублирует ранее созданную в БД запись')
    def test_create_couriers_with_login_in_database(self, new_courier_return_login_password):
        data = new_courier_return_login_password
        login = data[0]

        data_create = {
            "login": login,
            "password": "12345"
        }
        response = requests.post(f'{Urls.URL_SCOOTER}{Endpoints.CREATE_COURIER}', data=data_create)
        assert response.status_code == 409 and response.text == '{"message": "Этот логин уже используется"}'

