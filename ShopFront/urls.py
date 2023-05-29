from django.urls  import path
from .views import *

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<int:product_id>/',product_detail, name='product_detail'),
]



