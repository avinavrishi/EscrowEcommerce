from django.db import models
from django.contrib.auth import get_user_model



class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(('Profile Picture'), blank=True, null=True,upload_to=".")
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    walletBalance = models.IntegerField( default = True, null= True)


    def __str__(self):
        return self.user.username

class Product(models.Model):
	#image, type, rating
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255, default='new')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    products = models.ManyToManyField('Product' , related_name='carts')


    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"CartItem: {self.product.name} (Quantity: {self.quantity})"


class ShippingAddress(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)

class BillingAddress(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)

class PaymentMethod(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    payment_options = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('bitcoin', 'Bitcoin'),
    ]
    payment_method = models.CharField(max_length=20, choices=payment_options)
    #created_at = models.DateTimeField(auto_now_add=True)


class DepositRecord(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    payment_currency = models.CharField(max_length=20)
    deposit_amount = models.IntegerField()
    transaction_id = models.CharField(max_length= 100, unique=True)
    status = models.CharField(max_length=20, null= True, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class WithdrawalRequest(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    withdraw_amount = models.IntegerField()

    payment_method = models.CharField(max_length=20)
    wallet_address = models.CharField(max_length=100, null=True, blank=True)

    status = models.CharField(max_length=20, null= True, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='orders')
    buyer_email = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, null= True, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} - User: {self.user.username}"



