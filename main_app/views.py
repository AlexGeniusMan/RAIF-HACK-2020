import requests
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import base64
from .models import *
from .serializers import *
from skimage.transform import rescale
import json
from datetime import datetime


# import qrcode
# from io import BytesIO
# from django.core.files import File
# from PIL import Image, ImageDraw
# from qrcode.image.pure import PymagingImage
# from PIL import Image


class CheckOrderStatusView(APIView):
    """
    Checks order status
    """


class CreateProductRefView(APIView):
    """
    Creates fast and slow QR-codes
    """

    def post(self, request, *args, **kwargs):
        url = 'https://devgang.ru/?admin_email=' + str(request.data.get('admin_email')) + '&product_name=' + str(
            request.data.get('product_name')) + '&nickname=' + str(request.data.get('nickname'))

        # qr = qrcode.QRCode(version=1, box_size=5, border=5)
        # qr.add_data(url)
        # qr.make(fit=True)
        # img = qr.make_image(fill='black', back_color='white')
        # img.save('qr_code_temp.png')

        order = Order(nickname=str(request.data.get('nickname')), url=url)
        order.save()

        print(order.qr_code)

        with open('qr_code_temp.png', "rb") as image_file:
            qr_slow = base64.b64encode(image_file.read())

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        json_temp = {
            "additionalInfo": "kriper2004",
            "amount": 3,
            "createDate": "2019-07-22T09:14:38.107227+03:00",
            "currency": "RUB",
            "order": dt_string,
            "paymentDetails": "Назначение платежа",
            "qrType": "QRDynamic",
            "sbpMerchantId": "MA543301"
        }
        str_temp = json.dumps(json_temp)

        url = "https://test.ecom.raiffeisen.ru/api/sbp/v1/qr/register"

        payload = str_temp
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        dict_temp = json.loads(response.text)
        print(dict_temp)
        qr_fast = dict_temp['qrUrl']
        qr_fast_id = dict_temp['qrId']

        return Response({
            'qr_fast_id': qr_fast_id,
            'qr_fast': qr_fast,
            'qr_slow': 'http://127.0.0.1:8000/media/' + str(order.qr_code)
        })


class ShowStoreView(APIView):
    """
    Shows current store
    """

    def get(self, request, store_pk):
        store = Store.objects.get(pk=store_pk)

        serializer = StoreSerializer(store, context={'request': request})
        return Response(serializer.data)


class ShowProductView(APIView):
    """
    Shows current product
    """

    def get(self, request, product_pk):
        product = Product.objects.get(pk=product_pk)

        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
