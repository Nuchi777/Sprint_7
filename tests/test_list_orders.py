import allure
import requests
from data import Urls
from data import Endpoints


class TestListOrders:
    @allure.title('При получении списка заказов в тело ответа возвращается список заказов')
    def test_return_list_orders_in_body(self):
        response = requests.get(f'{Urls.URL_SCOOTER}{Endpoints.LIST_ORDERS}')
        list_orders = response.json()['orders']
        assert response.status_code == 200 and len(list_orders) != 0