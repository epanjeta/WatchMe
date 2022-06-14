from django.utils import timezone 
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from watch.models import Watch
from django.contrib import messages

# Create your views here.

def allFilled(x, y, z, xx, yy, zz):
        if len(x) == 0 or len(y) == 0 or len(z) == 0 or len(xx) == 0 or len(yy) == 0 or len(zz) == 0:
                return False
        else:
                return True

def add_to_cart(request, productId):
        #Finding Cart of a User
        current_user = request.user
        cart = get_object_or_404(Cart, user = current_user, isActive = True)
        #Finding the Product
        product = get_object_or_404(Watch, pk = productId)
        print(cart)
        print(product)
        cartItem = CartItem.create(cart, product)
        cartItem.save()
        cart.total = cart.total + product.price
        cart.save()
        print(cartItem)
        return redirect('cart')

def cart_view(request):
        current_user = request.user
        if current_user.is_authenticated:
                cart = get_object_or_404(Cart, user = current_user, isActive = True)
                cartItems = CartItem.objects.filter(cart = cart)
                cartItemsList = list(cartItems)
                products = []
                for item in cartItemsList:
                        product = get_object_or_404(Watch, pk = item.product_id)
                        products.append(product)
                context = {'products' : products,
                        'total' : cart.total}
                return render(request, 'cart/cart.html', context=context)
        else:
             context = {'message': 'Please log in so you can access your cart'}
             return render(request, 'pages/permission_denied.html', context)   

def remove_from_cart(request, productId):
        current_user = request.user
        cart = get_object_or_404(Cart, user = current_user, isActive = True)
        product = get_object_or_404(Watch, pk = productId)
        cartItems = CartItem.objects.filter(cart = cart)
        for cartItem in cartItems:
                if cartItem.product.id == productId:
                        cartItemDelete = CartItem.objects.get(id = cartItem.id)
                        cartItemDelete.delete()
                        cart.total = cart.total - product.price
                        cart.save()
                        break
        return redirect('cart')

def checkout_view(request):
        #ako nije log-inovan
        current_user = request.user
        if not current_user.is_authenticated:
                context = {'message': 'Please log in so you can access your cart and checkout'}
                return render(request, 'pages/permission_denied.html', context)         
        #ako nema artikala u korpi
        cart = get_object_or_404(Cart, user = current_user, isActive = True)
        cartItems = CartItem.objects.filter(cart = cart)
        cartItemsList = list(cartItems)
        if len(cartItemsList) == 0:
                context = {'message': 'You dont have any products in your cart'}
                return render(request, 'pages/permission_denied.html', context)

        if request.method == 'POST':
                street = request.POST['street']
                phonenumber = request.POST['phonenumber']
                postal = request.POST['postalcode']
                creditcard = request.POST['creditcard']
                expdate = request.POST['expdate']
                cvc = request.POST['cvc']
                
                if not allFilled(street, phonenumber, postal, creditcard, expdate, cvc):
                       messages.error(request, 'Please fill out all fields') 
                       return redirect('checkout')
                
                #Postaviti isActive = False
                
                
                cart.isActive = False
                cart.dateFinished = timezone.now()
                print(timezone.now())
                print(cart.dateFinished)
                cart.save()
                #Kreirati novu praznu korpu
                newCart = Cart.create(current_user)
                newCart.save()
                #Smanjiti broj artikala za 1
                
                for item in cartItemsList:
                        product = get_object_or_404(Watch, pk = item.product_id)
                        product.availableItems = product.availableItems - 1
                        product.save()


                #Poslati poruku za kraj
                context = {'message': 'You have successfully finished your shopping!'}
                return render(request, 'pages/success.html', context)

        else:
                return render(request, 'cart/checkout.html')


