"""azweb_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from shop_basket.views import Index, BasketPage, statistic_page, raise_price, OrderView

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('basket_page/', BasketPage.as_view(), name='basket_page'),
    path('add_order_to_basket/<int:pk>', OrderView.as_view(), name='add_order_to_basket'),
    path('raise_price/<int:pk>', raise_price, name='raise_price'),

    path('statistic_page/<int:pk>', statistic_page, name='statistic_page'),

    path('admin/', admin.site.urls),
]
