from django.db import models
from django.utils.translation import gettext_lazy as _

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw


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

# class OrderManager(models.Manager):
#     def create_order(self, url, order_owner, qr_code):
#         order = self.create(url=url, order_owner=order_owner, qr_code=qr_code)
#         # do something with the book
#         return order
#
#
# class Order(models.Model):
#     url = models.CharField(_('URL'), max_length=100)
#     order_owner = models.CharField(_('Клиент'), max_length=200)
#     qr_code = models.ImageField(_('QR-код'), upload_to='qr_codes', blank=True)
#
#     objects = OrderManager()
#
#     def __str__(self):
#         return str(self.order_owner)


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



class Order(models.Model):
    nickname = models.CharField(_("Ник покупателя"), max_length=64, blank=False)
    url = models.CharField(_('URL'), max_length=200, blank=True)
    qr_code = models.ImageField(_('QR slow'), blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.nickname

    def save(self, *args, **kwargs):
        qr = qrcode.QRCode(version=1, box_size=5, border=5)
        qr.add_data(self.url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        canvas = Image.new('RGB', (256, 256), 'white')
        canvas.paste(img)
        fname = f'qr_code-{self.nickname}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


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
        verbose_name = 'Сервер'
        verbose_name_plural = 'Сервера'

    def __str__(self):
        return self.name
