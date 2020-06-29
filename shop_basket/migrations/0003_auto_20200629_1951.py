# Generated by Django 3.0.7 on 2020-06-29 19:51

from django.db import migrations, models
import shop_basket.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_basket', '0002_auto_20200622_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='price',
            field=models.PositiveSmallIntegerField(validators=[shop_basket.models.validate_price], verbose_name='price'),
        ),
    ]
