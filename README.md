# Sprint_7
# Яндекс Самокат
## Это сервис по аренде самокатов!

### Использованные библиотеки и зависимости:
1. [x] allure-pytest==2.13.2
2. [x] pytest==7.4.3
3. [x] requests==2.31.0

### Описание тестов:

##### Courier - Создание курьера (POST - /api/v1/courier):
* test_can_create_courier
#Регистрация в приложении пройдет успешно, если валидными данными заполнены все поля

* test_cannot_create_two_identical_couriers
#Регистрация в приложении пройдет неуспешно, если повторно создать пользователя с теми же параметрами

* test_create_couriers_fill_not_all_required_field
#Регистрация в приложении пройдет неуспешно, если поле login или password пустое

* test_create_couriers_required_field_login_or_password_not_sending
#Регистрация в приложении пройдет неуспешно, если поле login или password не передано

* test_create_couriers_with_login_in_database
#Регистрация в приложении пройдет неуспешно, если поле login дублирует ранее созданную в БД запись

##### Courier - Логин курьера в системе (POST - /api/v1/courier/login):
* test_login_couriers
#Авторизация в приложении пройдет успешно, если валидными данными заполнены все обязательные поля

* test_login_couriers_required_field_login_empty
#Авторизация в приложении пройдет неуспешно, если обязательное поле login пустое

* test_login_couriers_required_field_password_empty
#Авторизация в приложении пройдет неуспешно, если обязательное поле password пустое

* test_login_couriers_field_login_incorrect
#Авторизация в приложении пройдет неуспешно, если обязательное поле login заполнено не верно

* test_login_couriers_field_password_incorrect
#Авторизация в приложении пройдет неуспешно, если обязательное поле password заполнено не верно

* test_login_couriers_required_field_login_not_sending
#Авторизация в приложении пройдет неуспешно, если обязательное поле login не передано

* test_login_couriers_required_field_password_not_sending
#Авторизация в приложении пройдет неуспешно, если обязательное поле password не передано

* test_login_couriers_non_existent_user
#Авторизация в приложении пройдет неуспешно, если авторизоваться под несуществующим пользователем

* test_login_couriers_return_id
#Успешный запрос возвращает id пользователя в теле ответа

##### Courier - Получение списка заказов (GET - /api/v1/orders):
* test_create_order_can_choose_scooter_colors_black_or_grey
#При оформлении заказа можно указать один из цветов самоката