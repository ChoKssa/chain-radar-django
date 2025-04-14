from django.urls import path
from . import views

urlpatterns = [
    path('cryptos/', views.crypto_list, name='crypto_list'),
    path('api/cryptos/', views.crypto_list_json, name='crypto_list_json'),
    path('api/cryptos/add/', views.add_crypto, name='crypto_add'),
    path('cryptos/<int:pk>/', views.crypto_detail, name='crypto_detail'),
    path('comparator/', views.crypto_comparator, name='crypto_comparator'),
]
