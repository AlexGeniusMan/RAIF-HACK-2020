from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    img = models.ImageField(_("Фото товара"), null=True, upload_to='media/api/products/')
    name = models.CharField(_("Название товара"), max_length=64, blank=False)
    price = models.IntegerField(_("Цена продукта"), blank=False)

    store = models.ForeignKey('Store', on_delete=models.CASCADE, verbose_name='Магазин', related_name='products',
                              null=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(_("Название магазина"), max_length=64, blank=False)
    email = models.EmailField(_("Email администратора"), blank=False)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name
