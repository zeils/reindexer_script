# Реиндексация документов курьера

Запуск -> main.py

[204] код при реиндексации - всё ок

Перед первым запуском убедитесь что у вас последняя версия хрома и селениума

В consts.py внесите свой логин/пароль от grlog-prod и courier.esphere.ru.

# Методы
Get_data() - заходит через selenium в грейлог, и скачивает выборку документов на реиндексацию за сутки

Use_reg() - проходит по выборке регулярными выражениями и кладёт номера документов в файл done.txt

Get_courier_cookie() - заходит через selenium в курьер и берет ваши куки для реиндексации, возвращает eSphereAuth, clinetID 

Reindexer() - проходит по done.txt и post запросом реиндексирует документы

# Дополнительно
Можно поднять значение переменной waiting_time если грйлог/курьер долго грузятся и выдают ошибку

При необходимости реиндексации больше чем за сутки необходимо в методе Get_data() поменять значение переменной graylog_filter_url

# Ошибки

[400-403] код при реиндексации -> проблема с куками/авторизацией в курьере

Ошибка find_element -> Поменялась UI, необходимо смотреть что именно

Ошибка session not created: Version... -> Ошибка версий selenium/chrome, попробуйте обновить до последней версии chrome браузер и пакет selenium
