from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from django import forms

from .models import Profile, Product



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'quantity']



class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'birth_date']


class ShippingAddressForm(forms.Form):
    address_line1 = forms.CharField(label='Address Line 1')
    address_line2 = forms.CharField(label='Address Line 2', required=False)
    city = forms.CharField(label='City')
    state = forms.CharField(label='State')
    postal_code = forms.CharField(label='Postal Code')

class BillingAddressForm(forms.Form):
    address_line1 = forms.CharField(label='Address Line 1')
    address_line2 = forms.CharField(label='Address Line 2', required=False)
    city = forms.CharField(label='City')
    state = forms.CharField(label='State')
    postal_code = forms.CharField(label='Postal Code')

class PaymentMethodForm(forms.Form):
    payment_options = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
    ]
    payment_method = forms.ChoiceField(choices=payment_options, widget=forms.RadioSelect)