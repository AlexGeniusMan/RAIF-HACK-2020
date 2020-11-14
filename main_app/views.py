from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *


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
