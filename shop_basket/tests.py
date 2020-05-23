from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
# Create your tests here.

c = Client()


class TestAdmin(TestCase):
    def test_anonymous_cannot_see_page(self):
        response = self.client.get(reverse("basket_page"))
        self.assertRedirects(response, "/accounts/login/?next=/basket_page/")

    def test_user_page(self):
        user = User.objects.create_user("anyuser","some_pass")
        self.client.force_login(user=user)
        response = self.client.get(reverse("basket_page"))
        self.assertEqual(response.status_code, 200)


class TestMainPage(TestCase):
    def test_index(self):
        index = c.get('/')
        self.assertEqual(index.status_code, 200)


class TestAddStuf(TestCase):
    def test_ok(self):
        add_stuff = c.post('/add_stuff_to_basket/1', {'title': ['vada'], 'price': ['12']})
        self.assertEqual(add_stuff.status_code, 302)


class TestTtitle(TestCase):
    def test_get_stat(self):
        stuff = c.get('/statistic_page/1', {'title': ['vada'], 'price': ['12']})
        self.assertEqual(stuff.status_code, 302)
