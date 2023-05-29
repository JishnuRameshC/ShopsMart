from django.urls  import path
from .views import *

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<int:product_id>/',product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('update-cart/', update_cart, name='update_cart'),
    path('checkout/', checkout, name='checkout'),


]



