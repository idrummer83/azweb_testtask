from django import forms
from .models import Basket


class BasketForm(forms.ModelForm):
    price = forms.IntegerField(min_value=1, label='price')

    class Meta:
        model = Basket
        fields = ['title']