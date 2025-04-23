from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, FarmerProfile, BuyerProfile
from cart_app.models import ShippingAddress
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email',  'place', 'phone_number', 'profile_pic')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'email',
            'user_type',
            'place',
            'phone_number',
            'profile_pic',
            Submit('submit', 'Register')
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
           
        return user

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Login')
        )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'place', 'phone_number', 'profile_pic')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'email',
            'place',
            'phone_number',
            'profile_pic',
            Submit('submit', 'Update Profile')
        )
        self.fields['username'].disabled = True
        self.fields['email'].disabled = True
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = ('farm_name', 'location', 'about')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'farm_name',
            'location',
            'about',
            Submit('submit', 'Update Farmer Profile')
        )

class BuyerProfileForm(forms.ModelForm):
    class Meta:
        model = BuyerProfile
        fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Submit('submit', 'Update Buyer Profile')
        )

class AddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'first_name',
            'last_name',
            'address1',
            'address2',
            'city',
            'state',
            'country',
            'postal_code',
            'phone_number',
            'default',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'address1',
            'address2',
            'city',
            'state',
            'country',
            'postal_code',
            'phone_number',
            'default',
            Submit('submit', 'Save Address')
        )

    def clean_postal_code(self):
        postal_code = self.cleaned_data['postal_code']
        if len(postal_code) < 3:
            raise forms.ValidationError("Postal code is too short.")
        return postal_code

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if country.lower() == "select country":
            raise forms.ValidationError("Please select a valid Country")
        return country