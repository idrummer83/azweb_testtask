from django import forms
from .models import Basket


class OrderForm(forms.ModelForm):

    class Meta:
        model = Basket
        fields = ('user', 'title', 'price')

    def clean_title(self):
        data = self.cleaned_data['title']
        if len(data) <= 2:
            raise forms.ValidationError("Too short title for order!")
        else:
            return data

    def clean_price(self):
        data = self.cleaned_data['price']
        if data <= 1:
            raise forms.ValidationError("Number must be positive and more then 1!")
        else:
            return data
