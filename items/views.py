from django.shortcuts import render
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from .models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        item_id = self.kwargs["pk"]
        items = Item.objects.get(id=item_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': items.price,
                        'product_data': {
                            'name': items.name
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "item_id": items.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


class BuyItem(DetailView):
    model = Item
    template_name = "items/buyitem.html"
    slug_url_kwarg = 'item_slug'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super(BuyItem, self).get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class AllItems(ListView):
    model = Item
    template_name = 'items/index.html'
    context_object_name = 'items'


class SuccessView(TemplateView):
    template_name = "items/success.html"


class CancelView(TemplateView):
    template_name = "items/cancel.html"
