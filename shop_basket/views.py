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


class BasketView(LoginRequiredMixin, TemplateView):
    template_name = 'basket_page.html'
    # form_class = BasketForm
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.extra_context['form'] = BasketForm()

        return super(BasketView, self).get(request)

    def post(self, request, pk):
        form = BasketForm(request.POST or None)

        if form.is_valid():
            price = form.cleaned_data['price']
            title = form.cleaned_data['title']
            Basket.objects.create(user_id=pk, price=price, title=title).save()
            return redirect(f'/statistic_page/{request.user.id}')
        else:
            messages.error(request, form.errors)
            return redirect('/basket_page/')


@login_required(login_url='/accounts/login/')
def statistic_page(request, pk):
    all_orders = Basket.objects.all()
    all_user_orders = Basket.objects.filter(user_id=pk)
    max_user_price = all_user_orders.aggregate(Max('price'))
    full_user_price = all_user_orders.aggregate(all_sum=Sum('price'))
    middle_user_price = all_user_orders.aggregate(Avg('price'))

    conditionby_user_title_sum = Basket.objects.filter(Q(user_id=pk) & Q(title__length__gte=3)).aggregate(all_sum=Sum('price'))
    conditionby_price_greater = Basket.objects.filter(Q(price__gte=50)).aggregate(all_sum=Sum('price'))

    if conditionby_user_title_sum:
        condition = conditionby_user_title_sum['all_sum'] + full_user_price['all_sum']
    else:
        condition = conditionby_price_greater
    context = {
        'all_orders': all_orders.count(),
        'all_user_orders': all_user_orders,
        'all_user_orders_number': all_user_orders.count(),
        'max_user_price': max_user_price['price__max'],
        'middle_user_price': round(middle_user_price['price__avg'], 2),
        'full_user_price': full_user_price['all_sum'],
        'condition': condition,
    }
    return render(request, 'statistic_page.html', context)


def raise_price(request, pk):
    for i in Basket.objects.filter(user_id=pk):
        Basket.objects.filter(id=i.id).update(price=F('price') + 1)
    return redirect(f'/statistic_page/{request.user.id}')
