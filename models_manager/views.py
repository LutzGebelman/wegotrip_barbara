from datetime import datetime
from uuid import UUID
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Order, Payment, PaymentStatus
from ast import literal_eval
import requests

@require_GET
def get_products_list(request: HttpRequest) -> HttpResponse:
    list_of_products = [model_to_dict(i) for i in Product.objects.all()]
    return HttpResponse(list_of_products)

@csrf_exempt
@require_POST
def post_to_cart(request: HttpRequest) -> HttpResponse:
    list_of_elements = literal_eval(request.body.decode())
    timestamp = datetime.now()
    list_of_prods = [Product.objects.get(pk=name) for name in list_of_elements]
    total_price = sum([prod.price for prod in list_of_prods])

    my_order = Order.objects.create(
        total_price = total_price,
        time_created = timestamp,
        time_confirmed = timestamp,
    )
    
    for prod in list_of_prods:
        my_order.product.add(prod)

    return HttpResponse(
        str({
        "timestamp": timestamp,
        "total_price": total_price
        })
    )

@csrf_exempt
def confirm_order(request, object_str):
    object = Order.objects.get(pk=UUID(object_str).hex)
    object.status_str = "CONFIRMED"
    object.time_confirmed = datetime.now()
    object.save()
    requests.post("https://webhook.site/36693e00-8f59-4f7b-9a85-1d1e7ddde4d4", data={
        'id': object.id,
        'amount': object.total_price,
        'date': object.time_confirmed
    })
    return HttpResponse(object)
    
@csrf_exempt
@require_POST
def post_payment(request: HttpRequest) -> HttpResponse:
    order_uuid = UUID(literal_eval(request.body.decode())['uuid']).hex
    order = (Order.objects.get(pk=order_uuid))
    obj = Payment.objects.create(
        order = order,
        total = order.total_price,
        status = PaymentStatus.PAID,
        payment_method = 'sber'
    )


    return HttpResponse(str(model_to_dict(obj)))
