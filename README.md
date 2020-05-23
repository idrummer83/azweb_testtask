# azweb_testtask
Python 3.6+; Django 3; Tests -- create simple buyer's basket

Стандартный логин
Пользователь должен иметь возможность залогиниться. Никаких требований к логину нет, использование готового решения от Джанго допустимо.
Регистрация не нужна, предполагается, что все пользователи создаются через админку или shell
Данная страница не нуждается в тестировании.

“Корзина”
Доступна только залогиненному пользователю.

Пользователь имеет возможность написать название товара, указать цену и отправить данные на сервер.

Данные должны валидироваться:
Цена позитивное число
Название больше или равно 2 символам

При наличии неправильных данных в форме: пользователь должен увидеть ошибки. Внешний вид роли не играет, но они должны выводиться.
При правильном вводе данных пользователь перенаправляется на страницу “Статистика”
Данные сохраняются в базе данных.
“Статистика”
Доступна только залогиненному пользователю.

Пользователь на этой странице видит следующие данные:
Общее количество товаров, которые ввел пользователь
Общее количество товаров, которое было введено в системе
Максимальную цену, которую ввел пользователь
Среднюю цену всех продуктов всех пользователей
Сумму цены всех товаров, которые ввел пользователь
Сумму всех товаров, которые ввел пользователь И длина имени которых составляет больше 3 знаков ИЛИ цена которых больше 50, независимо от того, кто их создал

Пользователь также видит здесь кнопку “Поднять цену”. При нажатии на эту кнопку, ко всем ценам всех товаров, которые создал пользователь, добавляется 1.
