from django.contrib import admin
from .models import Product,Category, Customer, Order, OrderItem
# Register your models here.

from django.contrib import admin
from .models import Product, Category, Customer, Order, OrderItem

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
