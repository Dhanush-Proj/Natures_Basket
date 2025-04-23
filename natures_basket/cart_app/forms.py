from django import forms
from .models import ShippingAddress  # Assuming ShippingAddress is in the same app

class CheckoutForm(forms.ModelForm):
    """
    A form for collecting shipping information during checkout.
    """

    class Meta:
        model = ShippingAddress
        fields = ['first_name','last_name','address1','address2','city','state','country','postal_code','phone_number']

    # Optional: Add any custom validation or field modifications here

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from the view
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            # Try to pre-fill the form with the user's default shipping address
            try:
                default_address = ShippingAddress.objects.get(user=user, default=True)
                self.fields['first_name'].initial = default_address.first_name
                self.fields['last_name'].initial = default_address.last_name
                self.fields['address1'].initial = default_address.address1
                self.fields['address2'].initial = default_address.address2
                self.fields['city'].initial = default_address.city
                self.fields['state'].initial = default_address.state
                self.fields['country'].initial = default_address.country
                self.fields['postal_code'].initial = default_address.postal_code
                self.fields['phone_number'].initial = default_address.phone_number
            except ShippingAddress.DoesNotExist:
                pass  # User has no default shipping address
