from django.db import models
from django.contrib.auth.models import AbstractUser

# Пользователь
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('manager', 'Менеджер'),
        ('client', 'Клиент'),
    ]
    rol = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    fio = models.CharField(max_length=200, blank=True)

# Тип товара
class TipTovara(models.Model):
    nazvanie = models.CharField(max_length=100)

# Категория
class Kategoriya(models.Model):
    nazvanie = models.CharField(max_length=100)

# Поставщик
class Postavschik(models.Model):
    nazvanie = models.CharField(max_length=200)

# Производитель
class Proizvoditel(models.Model):
    nazvanie = models.CharField(max_length=200)

# Товар
class Tovar(models.Model):
    artikul = models.CharField(max_length=20, primary_key=True)
    tip_tovara = models.ForeignKey(TipTovara, on_delete=models.CASCADE)
    tsena = models.DecimalField(max_digits=10,decimal_places=2)
    postavschik = models.ForeignKey(Postavschik, on_delete=models.CASCADE)
    proizvoditel = models.ForeignKey(Proizvoditel, on_delete=models.CASCADE)
    kategoriya = models.ForeignKey(Kategoriya, on_delete=models.CASCADE)
    skidka = models.IntegerField()
    ostatok = models.IntegerField()
    opisanie = models.TextField(blank=True)
    foto = models.ImageField(upload_to='', blank=True)

# Пункт выдачи
class PunktVydachi(models.Model):
    nazvanie = models.TextField()

# Статус заказа
class StatusZakaza(models.Model):
    nazvanie = models.CharField(max_length=50)

# Заказ
class Zakaz(models.Model):
    polzovatel = models.ForeignKey(User, on_delete=models.CASCADE)
    punkt_vydachi = models.ForeignKey(PunktVydachi, on_delete=models.CASCADE)
    data_zakaza = models.DateField()
    data_dostavki = models.DateField()
    kod_polucheniya = models.CharField(max_length=10)
    status = models.ForeignKey(StatusZakaza, on_delete=models.CASCADE)

# Товар в заказе
class TovarVZakaze(models.Model):
    zakaz = models.ForeignKey(Zakaz, on_delete=models.CASCADE)
    tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE)
    kolichestvo = models.IntegerField()
