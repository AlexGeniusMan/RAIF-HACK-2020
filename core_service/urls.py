"""core_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import main_app.views as main_app
from .yasg import urlpatterns as doc_url

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/get_qr', main_app.CreateProductRefView.as_view()),  # GET - gets current product

    path('api/products/<int:product_pk>', main_app.ShowProductView.as_view()),  # GET - gets current product
    path('api/stores/<int:store_pk>', main_app.ShowStoreView.as_view()),  # GET - gets current store

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += doc_url