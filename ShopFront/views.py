from django.shortcuts import render, get_object_or_404, redirect
from .models import *


def product_list(request):
    products = Product.objects.all()
    return render(request, 'ShopFront/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'ShopFront/product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Retrieve cart data from the session or initialize as an empty dictionary
    cart = request.session.get('cart', {})

    # Increment the quantity if the product is already in the cart, otherwise set it to 1
    cart[product_id] = cart.get(product_id, 0) + 1

    # Update the cart data in the session
    request.session['cart'] = cart
    request.session.modified = True

    # Redirect to a relevant page (e.g., product listing or cart view)
    return redirect('product_list')


def view_cart(request):
    # Retrieve cart data from the session or initialize as an empty dictionary
    cart = request.session.get('cart', {})

    # Retrieve the product objects corresponding to the cart items
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)

    # Calculate the total amount
    total_amount = 0
    for product in products:
        quantity = cart[str(product.id)]
        total_amount += product.price * quantity

    # Render the template with cart data
    return render(request, 'ShopFront/cart.html', {'cart': cart, 'products': products, 'total_amount': total_amount})


def update_cart(request):
    cart = request.session.get('cart', {})

    # Retrieve the updated quantities from the request POST data
    updated_quantities = request.POST.getlist('quantity')

    # Iterate over the cart items and update the quantities
    for product_id, quantity in zip(cart.keys(), updated_quantities):
        cart[product_id] = int(quantity)

    # Update the cart data in the session
    request.session['cart'] = cart
    request.session.modified = True

    # Redirect to the cart view
    return redirect('view_cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    # Remove the specified product from the cart
    if str(product_id) in cart:
        del cart[str(product_id)]

    # Update the cart data in the session
    request.session['cart'] = cart
    request.session.modified = True

    # Redirect to the cart view
    return redirect('view_cart')


def checkout(request):
    cart = request.session.get('cart', {})

    # Retrieve the product objects corresponding to the cart items
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)

    # Calculate the total amount
    total_amount = 0
    for product in products:
        quantity = cart[str(product.id)]
        total_amount += product.price * quantity

    if request.method == 'POST':
        # Create an order object
        order = Order.objects.create(total_amount=total_amount)

        # Store relevant information from the cart in the order object
        for product in products:
            quantity = cart[str(product.id)]
            order.items.create(product=product, quantity=quantity, price=product.price)

        # Clear the cart data from the session
        del request.session['cart']

        # Redirect to a success or thank you page
        return redirect('order_success')

    # Render the checkout template
    return render(request, 'ShopFront/checkout.html', {'cart': cart, 'products': products, 'total_amount': total_amount})



