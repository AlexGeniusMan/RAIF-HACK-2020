from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import base64
from .models import *
from .serializers import *
from skimage.transform import rescale


# import qrcode
# from io import BytesIO
# from django.core.files import File
# from PIL import Image, ImageDraw
# from qrcode.image.pure import PymagingImage
# from PIL import Image


class CreateProductRefView(APIView):
    """
    Creates QR-code
    """

    def post(self, request, *args, **kwargs):
        url = 'https://devgang.ru/?admin_email=' + str(request.data.get('admin_email')) + '&product_name=' + str(
            request.data.get('product_name')) + '&nickname=' + str(request.data.get('nickname'))

        qr = qrcode.QRCode(version=1, box_size=5, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save('qr_code_temp.png')

        with open('qr_code_temp.png', "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read())

        return Response({
            'qr_code': encoded_image
        })

        # ej_response = requests.post(
        #     'http://188.120.248.65:8065/ejapi/tasks/run',
        #     json={
        #         'key': key,
        #         'language': language,
        #         'code': code,
        #         'tests': tests,
        #         'time_limit_millis': time_limit_millis,
        #         'user_id': user_id
        #     }
        # )

        # ej_response = ej_response.json()

        # if ej_response['body'] == '':
        #     data = {
        #         'status': ej_response['status'],
        #         'error': ej_response['error']
        #     }

        #     return Response(json.dumps(data))
        # else:
        #     is_done = True
        #     tests_count = len(ej_response['body'])
        #     good_tests_count = 0
        #     for el in ej_response['body']:
        #         if not el['status']:
        #             is_done = False
        #         else:
        #             good_tests_count += 1
        #
        #     data = {
        #         'status': ej_response['status'],
        #         'mark': int(good_tests_count / tests_count * 100)
        #     }
        #
        # if is_done:
        #     task_detail = TaskDetail.objects.get(task=request.POST['task_id'], students=request.user.id)
        #     task_detail.is_done = True
        #     task_detail.save()
        #
        # return Response(json.dumps(data))


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
