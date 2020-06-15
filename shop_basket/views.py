from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Basket

from .forms import BasketForm

# Create your views here.


class Index(TemplateView):
    template_name = 'index.html'


class BasketPage(LoginRequiredMixin, TemplateView):
    template_name = 'basket_page.html'


class BasketView(LoginRequiredMixin, FormView):
    template_name = 'basket_page.html'
    form_class = BasketForm

    def get(self, request, pk):
        return render(request, 'basket_page.html', {})

    def post(self, request, pk):
        form = BasketForm(request.POST or None)
        if form.is_valid():
            price = form.cleaned_data['price']
            title = form.cleaned_data['title']
            if len(title) <= 1:
                messages.error(request, 'title too short')
                return redirect('/basket_page/')

            if price == '' or int(price) < 0 or int(price) == 0:
                messages.error(request, 'price incorect')
                return redirect('/basket_page/')

            Basket.objects.create(user_id=pk, price=price, title=title).save()
            return redirect('/statistic_page/{}'.format(request.user.id))


@login_required(login_url='/accounts/login/')
def statistic_page(request, pk):
    all_stuff = Basket.objects.all()
    all_user_stuff = Basket.objects.filter(user_id=pk)
    max_user_price = max([i.price for i in all_user_stuff])
    full_user_price = sum([i.price for i in all_user_stuff])
    middle_user_price = sum([i.price for i in all_user_stuff])/all_user_stuff.__len__()

    condition = sum([i.price for i in all_user_stuff if len(i.title) > 3])
    condition1 = sum([i.price for i in all_stuff if i.price > 50])

    if condition > 0:
        cond = condition
    else:
        cond = condition1

    cxt = {
        'all_stuff': all_stuff.__len__(),
        'all_user_stuff': all_user_stuff,
        'all_user_stuff_num': len(all_user_stuff),
        'max_user_price': max_user_price,
        'middle_user_price': round(middle_user_price, 2),
        'full_user_price': full_user_price,
        'cond': cond,
    }
    return render(request, 'statistic_page.html', cxt)


def add_to_price(request, pk):
    all_user_stuff = Basket.objects.filter(user_id=pk)
    for i in all_user_stuff:
        i.price += 1
        Basket.objects.filter(id=i.id).update(price=i.price)
    return redirect('/statistic_page/{}'.format(request.user.id))
