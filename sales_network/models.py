from django.db import models


class NetworkNode(models.Model):
    NODE_TYPE_CHOICES = [
        ('factory', 'Завод'),
        ('retail', 'Розничная сеть'),
        ('ip', 'ИП'),
    ]

    name = models.CharField(max_length=255, verbose_name='Название')
    email = models.EmailField(verbose_name='Email')
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=255, verbose_name='Улица')
    house_number = models.CharField(max_length=20, verbose_name='Номер дома')
    node_type = models.CharField(max_length=10, choices=NODE_TYPE_CHOICES, verbose_name='Тип узла')
    provider = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='clients',
        verbose_name='Поставщик'
    )
    debt = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Задолженность перед поставщиком')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return self.name

    def get_level(self):
        level = 0
        current = self
        while current.provider:
            level += 1
            current = current.provider
        return level

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название продукта')
    model = models.CharField(max_length=255, verbose_name='Модель')
    release_date = models.DateField(verbose_name='Дата выхода на рынок', blank=True, null=True)
    node = models.ForeignKey(NetworkNode, on_delete=models.SET_NULL, blank=True, null=True, related_name='products', verbose_name='Звено сети')

    def __str__(self):
        return f"{self.name} ({self.model})"
