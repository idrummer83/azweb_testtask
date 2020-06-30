from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from shop_basket.models import Basket


class BasketViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test_user_1', email='test1@example.com', password='test_password_1')
        order = Basket.objects.create(user=user, title='Test order', price=12)

    def test_user_login(self):
        result = self.client.login(username='test_user_1', password='test_password_1')
        self.assertEqual(result, True)

        response = self.client.get(reverse('basket_page'))
        self.assertEqual(response.status_code, 200)

    def test_user_login_incorrect(self):
        result = self.client.login(username='test_', password='tesrd_')
        self.assertFalse(result, False)

        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_order_create(self):
        self.client.login(username='test_user_1', password='test_password_1')
        self.user = User.objects.filter(username='test_user_1').first()
        order = Basket.objects.create(user=self.user, title='Test order', price=22)

        response = self.client.get(reverse('statistic_page', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, 200)

    def test_order_errors(self):
        self.client.login(username='test_user_1', password='test_password_1')
        self.user = User.objects.filter(username='test_user_1').first()
        order_empty_title = Basket.objects.create(user=self.user, title='', price=22)
        self.assertRaises(ValidationError, order_empty_title.full_clean)

        order_title_short = Basket.objects.create(user=self.user, title='q', price=22)
        self.assertRaises(ValidationError, order_title_short.full_clean)

        order_price_zero = Basket.objects.create(user=self.user, title='qwe', price=0)
        self.assertRaises(ValidationError, order_price_zero.full_clean)

        order_price_small = Basket.objects.create(user=self.user, title='qweert', price=1)
        self.assertRaises(ValidationError, order_price_small.full_clean)


