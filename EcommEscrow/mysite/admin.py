from django.contrib import admin
from .models import Product, Cart,CartItem, ShippingAddress, BillingAddress, PaymentMethod, Profile, DepositRecord, WithdrawalRequest, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'created_at', 'created_by']
    list_filter = ['created_at']
    search_fields = ['name', 'description', 'category']



admin.site.register(Profile)
admin.site.register(Cart)

admin.site.register(DepositRecord)
admin.site.register(WithdrawalRequest)

admin.site.register(Order)

admin.site.register(CartItem)

admin.site.register(ShippingAddress)
admin.site.register(BillingAddress)
admin.site.register(PaymentMethod)