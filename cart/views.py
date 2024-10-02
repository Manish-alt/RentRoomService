from django.shortcuts import render, get_object_or_404
from .cart import Cart
from RentRoomCustomer.models import Product
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    
    return render(request, "cart_summary.html", {"cart_products":cart_products})

def cart_add(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get("product_id"))
        product = get_object_or_404(Product, id=product_id)
        
        cart.add(product = product)
        cart_quantity = cart.__len__()
        
        response = JsonResponse({'qty: ': cart_quantity})
        return response
    

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get("product_id"))
        
        cart.delete(product=product_id)
                        
    
        response = JsonResponse({'product_id: ': product_id})
        return response

def cart_update(request):
    return render(request, "cart_update", {})