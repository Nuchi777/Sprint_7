import json
import allure
import pytest
import requests
from data import Urls
from data import Endpoints


class TestCreateOrder:
    @allure.title('При оформлении заказа можно указать один из цветов самоката')
    @pytest.mark.parametrize("color", ['BLACK', 'GREY', "BLACK, GREY", ''])
    def test_create_order_can_choose_scooter_colors_black_or_grey(self, color):
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
        response = requests.post(f'{Urls.URL_SCOOTER}{Endpoints.CREATE_ORDER}', data=data_create_order_json)
        track_order = response.json()['track']
        assert response.status_code == 201 and response.text == f'{{"track":{track_order}}}'