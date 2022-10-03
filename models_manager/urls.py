from django.urls import path

from . import views

urlpatterns = [
    path('all_products', views.get_products_list, name='get_products_list'),
    path('make_an_order', views.post_to_cart, name='make_an_order'),
    path('make_payment', views.post_payment, name='make_payment'),
    path('confirm_order/<str:object_str>', views.confirm_order, name='confirm_order')
]