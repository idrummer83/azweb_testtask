from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Max, Avg, Sum, Q, F, CharField
from django.db.models.functions import Length
CharField.register_lookup(Length)
from .models import Basket

from .forms import BasketForm

# Create your views here.


class Index(TemplateView):
    template_name = 'index.html'


class BasketPage(LoginRequiredMixin, TemplateView):
    template_name = 'basket_page.html'

    def get(self, request):
        form = BasketForm()
        return render(request, 'basket_page.html', {'form': form})


class BasketView(LoginRequiredMixin, FormView):
    template_name = 'basket_page.html'
    form_class = BasketForm

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
    max_user_price = all_user_stuff.aggregate(Max('price'))
    full_user_price = all_user_stuff.aggregate(all_sum=Sum('price'))
    middle_user_price = all_user_stuff.aggregate(Avg('price'))

    condition = Basket.objects.filter(Q(user_id=pk) & Q(title__length__gte=3)).aggregate(all_sum=Sum('price'))
    condition1 = Basket.objects.filter(Q(price__gte=50)).aggregate(all_sum=Sum('price'))

    if condition:
        cond = condition['all_sum'] + full_user_price['all_sum']
    else:
        cond = condition1
    cxt = {
        'all_stuff': all_stuff.count(),
        'all_user_stuff': all_user_stuff,
        'all_user_stuff_num': all_user_stuff.count(),
        'max_user_price': max_user_price['price__max'],
        'middle_user_price': round(middle_user_price['price__avg'], 2),
        'full_user_price': full_user_price['all_sum'],
        'cond': cond,
    }
    return render(request, 'statistic_page.html', cxt)


def add_to_price(request, pk):
    all_user_stuff = Basket.objects.filter(user_id=pk)
    for i in all_user_stuff:
        Basket.objects.filter(id=i.id).update(price=F('price') + 1)
    return redirect('/statistic_page/{}'.format(request.user.id))
