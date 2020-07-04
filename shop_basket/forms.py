from django import forms
from .models import Basket, validate_title, validate_price


class OrderForm(forms.ModelForm):

    class Meta:
        model = Basket
        fields = ('user', 'title', 'price')

    def clean_title(self):
        if not validate_title(self.cleaned_data['title']):
            return self.cleaned_data['title']

    def clean_price(self):
        if not validate_price(self.cleaned_data['price']):
            return self.cleaned_data['price']
