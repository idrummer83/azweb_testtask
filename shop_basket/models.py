from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_basket', verbose_name='user')
    price = models.SmallIntegerField(verbose_name='price')
    title = models.CharField(max_length=250, verbose_name='stuff title')

    def __str__(self):
        return self.title
