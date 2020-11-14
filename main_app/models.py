from django.db import models
from django.utils.translation import gettext_lazy as _

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from qrcode.image.pure import PymagingImage


# class OrderManager(models.Manager):
#     def create_book(self, url, nickname):
#         book = self.create(url=url, order_owner=nickname)
#         # do something with the book
#         return book


# class Order(models.Model):
#     url = models.CharField('URL', max_length=100)
#     order_owner = models.CharField('OWNER', max_length=100)
#     qr_code = models.ImageField(upload_to='media/api/qr_codes/', blank=True)
#
#     # objects = OrderManager()
#
#     def __str__(self):
#         return self.url
#
#     def save(self, *args, **kwargs):
#         qrcode_img = qrcode.make(self.order_owner)
#         canvas = Image.new('RGB', (290, 290), 'white')
#         draw = ImageDraw.Draw(canvas)
#         canvas.paste(qrcode_img)
#         fname = f'qr_code-{self.order_owner}.png'
#         buffer = BytesIO
#         canvas.save(buffer, 'PNG')
#         self.qr_code.save(fname, File(buffer), save=False)
#         canvas.close()
#         super().save(*args, **kwargs)

class OrderManager(models.Manager):
    def create_order(self, url, order_owner, qr_code):
        order = self.create(url=url, order_owner=order_owner, qr_code=qr_code)
        # do something with the book
        return order


class Order(models.Model):
    url = models.CharField(_('URL'), max_length=100)
    order_owner = models.CharField(_('Клиент'), max_length=200)
    qr_code = models.ImageField(_('QR-код'), upload_to='qr_codes', blank=True)

    objects = OrderManager()

    # @classmethod
    # def create(cls, url, order_owner):
    #     order = cls(url, order_owner)
    #     # do something with the book
    #     return order

    def __str__(self):
        return str(self.order_owner)



    # def save(self, *args, **kwargs):
    #     qrcode_img = qrcode.make(self.url)
    #     canvas = Image.new('RGB', (512, 512), 'white')
    #     canvas.paste(qrcode_img)
    #     fname = f'qr_code-{self.order_owner}.png'
    #     buffer = BytesIO()
    #     canvas.save(buffer, 'PNG')
    #     self.qr_code.save(fname, File(buffer), save=False)
    #     canvas.close()
    #     super().save(*args, **kwargs)


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
