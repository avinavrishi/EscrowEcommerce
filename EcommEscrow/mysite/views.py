from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import Product, Cart, DepositRecord, WithdrawalRequest, Order, CartItem

from .forms import LoginForm, CreateUserForm, ShippingAddressForm, BillingAddressForm, PaymentMethodForm, AddProductForm

from uuid import uuid4


def index(request):
    products = Product.objects.all()
    return render(request, 'homepage.html', {'products': products})

@login_required
def profile(request):
    user = request.user

    context = {'user': user}
    return render(request, 'profile.html', context)


def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  # Redirect to the profile page after successful registration
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'signup.html', context)


    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the desired page after successful login
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('home')


#Prduct detail page view
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def cart(request):
    cart = request.user.cart
    cart_items = cart.cartitem_set.all()
    total_price = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if item_created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.user.cart
    cart_item = cart.cartitem_set.filter(product=product).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')




@login_required
def checkout(request):
    cart = request.user.cart
    cart_products = cart.products.all()
    total_price = sum(product.price for product in cart_products)

    if request.method == 'POST':

        profile = request.user.profile
        if profile.walletBalance >= total_price:

            profile.walletBalance -= total_price
            profile.save()



            buyer_email = request.POST.get('email')

            # Create an order object and save it
            order = Order(user=request.user, buyer_email=buyer_email, total_price = total_price )
            order.save()

            # Add cart products to the order
            for product in cart_products:
                order.products.add(product)

            # Clear the cart after placing the order
            cart.products.clear()

            return redirect('order_confirmation')
        else:
            return redirect('wallet')

    context = {
        'cart': cart,
        'cart_products': cart_products,
        'total_price': total_price,
    }
    return render(request, 'checkout.html', context)

@login_required
def order_confirmation(request):
    return render(request, 'order_confirmation.html')



@login_required
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            return redirect('product_detail', product.id)
    else:
        form = AddProductForm()
    
    context = {
        'form': form
    }
    return render(request, 'add_product.html', context)


@login_required
def user_product_list(request):
    user = request.user
    products = Product.objects.filter(created_by=user)
    context = {'products': products}
    return render(request, 'user_product_list.html', context)


@login_required
def wallet(request):
    balance = request.user.profile.walletBalance
    deposits = DepositRecord.objects.filter(user=request.user)
    withdrawals = WithdrawalRequest.objects.filter(user=request.user)
    return render(request, 'wallet.html', {'balance': balance, 'deposits': deposits, 'withdrawals': withdrawals})

@login_required
def add_balance(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        depositRecord = DepositRecord(user= request.user, payment_currency="USD", deposit_amount = amount, transaction_id=str(uuid4()))
        depositRecord.save()

        profile = request.user.profile
        profile.walletBalance += amount
        profile.save()
    return redirect('wallet')

@login_required
def withdraw_balance(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        profile = request.user.profile
        if profile.walletBalance >= amount:
            profile.walletBalance -= amount
            profile.save()

            withdrawal_request = WithdrawalRequest(user= request.user, withdraw_amount= amount, payment_method="BTC", wallet_address="testaddress")
            withdrawal_request.save()

    return redirect('wallet')


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'order_history.html', context)

@login_required
def approve_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.status == 'pending':
        order.status = 'approved'
        order.save()
    return redirect('order_history')