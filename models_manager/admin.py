from pyexpat import model
from django.contrib import admin

from .models import Order, Payment, Product


class CustomOrder(admin.ModelAdmin):
    change_form_template = "admin/barbara/models_manager/change_form.html"
    readonly_fields = ('status_str',)
    fieldsets = [
        (None, {'fields': ('status_str', 'id', 'total_price', 'product', 'time_confirmed')})
    ]

class CustomPayment(admin.ModelAdmin):
    readonly_fields = ('total',)


admin.site.register(Order, CustomOrder)
admin.site.register(Payment, CustomPayment)
admin.site.register(Product)