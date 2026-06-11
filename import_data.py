import csv, os, django

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from main.models import (
    TipTovara, Kategoriya, Postavschik, Proizvoditel,
    Tovar, User, TovarVZakaze, Zakaz, StatusZakaza, PunktVydachi
)

# Функция загрузки CSV
def load_csv(file_name, create_func, row_handler):
    with open(file_name, 'r', encoding='utf-8-sig') as file:
        for row in  csv.DictReader(file):
            create_func(**row_handler(row))

# Cправочники (с полями nazvanie)
for model, csv_file in [
    (TipTovara, 'tip_tovara.csv'),
    (Kategoriya, 'kategoriya.csv'),
    (Postavschik, 'postavschik.csv'),
    (Proizvoditel, 'proizvoditel.csv'),
    (PunktVydachi, 'punkt_vydachi.csv'),
    (StatusZakaza, 'status_zakaza.csv'),
]:
    load_csv(csv_file, model.objects.create, lambda r: {'nazvanie': r['nazvanie']})

# Пользователи (create_user хэширует пароль)
load_csv('user.csv', User.objects.create_user,
         lambda r: {
             'username': r['username'],
             'password': r['password'],
             'fio': r['fio'],
             'rol': {1: 'admin', 2: 'manager', 3: 'client'}[int(r['rol'])]
         })

# Товары, заказы, товары в заказе - все поля совпадают с CSV
load_csv('tovar.csv', Tovar.objects.create, lambda r: r)
load_csv('zakaz.csv', Zakaz.objects.create, lambda r: r)
load_csv('tovar_v_zakaze.csv', TovarVZakaze.objects.create, lambda r: r)
