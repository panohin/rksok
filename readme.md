## **Сервер на протоколе РКСОК 1.0**

РКСОК версии 1.0 состоит из четырёх команд:
ОТДОВАЙ — для возврата данных
УДОЛИ — для удаления данных
ЗОПИШИ — для создания и обновления данных
АМОЖНА? — для получения разрешения обработки команды от специальных органов.

Первые три команды предназначены для работы с клиентами, которые могут запрашивать возврат данных, их удаление и сохранение, а четвертая команда предназначена для общения сервера РКСОК с сервером специальных органов проверки всех запросов. Каждый запрос перед обработкой отправляется сначала на сервер проверки, и, если тот возвращает ответ МОЖНА, значит, сервер обрабатывает запрос. Если от сервера проверки пришёл любой другой ответ — клиенту возвращается этот ответ, а запрос дальше не обрабатывается.

Данные телефонной книги сохраняются в файл txt.





