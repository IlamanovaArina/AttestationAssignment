import logging
from django.db import models

from users.models import User

logger = logging.getLogger('sales_network')


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
    provider = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='clients',
                                 verbose_name='Поставщик')
    debt = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Задолженность перед поставщиком')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')

    def __str__(self):
        return self.name

    def get_level(self):
        level = 0
        current = self
        while current.provider:
            logger.info(f'Network: {current}, supplier found: {str(current.provider)}')
            level += 1
            logger.info(f'Raising the level for {current}. Current level: {level}')
            current = current.provider
        return level

    def save(self, *args, **kwargs):
        logger.info(f'Saving an object {self}')
        super().save(*args, **kwargs)
        logger.info(f'Object {self} saved successfully')


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название продукта')
    model = models.CharField(max_length=255, verbose_name='Модель')
    release_date = models.DateField(verbose_name='Дата выхода на рынок', blank=True, null=True)
    node = models.ForeignKey(NetworkNode, on_delete=models.SET_NULL, blank=True, null=True, related_name='products',
                             verbose_name='Звено сети')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')

    def save(self, *args, **kwargs):
        logger.info(f'Saving an object {self}')
        super().save(*args, **kwargs)
        logger.info(f'Object {self} saved successfully')

    def __str__(self):
        return f"{self.name} ({self.model})"
