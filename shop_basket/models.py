from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Create your models here.

def validate_title(value):
    if len(value) < 2:
        raise ValidationError(
            _('%(value)s is too short title for order'),
            params={'value': value},
        )


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_basket', verbose_name='user')
    price = models.PositiveSmallIntegerField(verbose_name='price')
    title = models.CharField(max_length=250, verbose_name='order title', validators=[validate_title])

    def __str__(self):
        return self.title
