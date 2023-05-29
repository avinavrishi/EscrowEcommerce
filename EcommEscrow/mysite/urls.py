from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.index, name="home"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('profile/', views.profile, name='profile'),

    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
     path('add_product/', views.add_product, name='add_product'),
     path('my_products/', views.user_product_list, name='user_product_list'),

    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),


    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),


    path('wallet/', views.wallet, name='wallet'),
    path('add-balance/', views.add_balance, name='add_balance'),
    path('withdraw-balance/', views.withdraw_balance, name='withdraw_balance'),

    path('order_history/', views.order_history, name='order_history'),
    path('approve-order/<int:order_id>/', views.approve_order, name='approve_order'),
]