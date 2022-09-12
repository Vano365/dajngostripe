from django.conf import settings # new
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new
from django.views.generic.base import TemplateView
import stripe
from django.shortcuts import render, redirect
from .models import *
import django

class HomePageView(TemplateView):
    template_name = 'payments/index.html'

    def get(self, request, *args, **kwargs):
        products = []
        products_db = Item.objects.order_by("currency")
        
        for p in products_db:
            if p.currency == 'usd':
                cur_name = "$"
            elif p.currency == 'eur':
                cur_name = "€"
            elif p.currency == 'rub':
                cur_name = "₽"
            products.append(
                {
                    'id': p.pk,
                    'name': p.name,
                    'price': p.price,
                    'cur_name': cur_name,
                    'cur': p.currency,
                    'description': p.description,
                }
            )

        cart_count = 0
        cart = Order.objects.all()

        for c in cart:
            cart_count += c.qty
        
        context = {
            'products': products,
            'products_len': len(products),
            'cart_count': cart_count,
        }
        
        return render(request, self.template_name, context=context)

class ProductPageView(TemplateView):
    template_name = 'payments/product.html'

    def get(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        product_db = Item.objects.get(pk=kwargs['id'])
        
        if product_db.currency == 'usd':
            cur_name = "$"
        elif product_db.currency == 'eur':
            cur_name = "€"
        elif product_db.currency == 'rub':
            cur_name = "₽"
        
        product = {
            'id': product_db.pk,
            'name': product_db.name,
            'price': product_db.price,
            'cur_name': cur_name,
            'cur': product_db.currency,
            'description': product_db.description,
        }

        cart_count = 0
        cart = Order.objects.all()

        for c in cart:
            cart_count += c.qty

        try:
            cart_product_count = Order.objects.get(item=product_db).qty
        except:
            cart_product_count = 0

        context = {
            'product': product,
            'cart_count': cart_count,
            'cart_product_count': cart_product_count,
        }
        
        return render(request, self.template_name, context=context)

class CartPageView(TemplateView):
    template_name = 'payments/cart.html'

    def get(self, request, *args, **kwargs):
        products = []
        products_db = Order.objects.all()
        total_usd = 0
        total_eur = 0
        total_rub = 0
        for p in products_db:
            if p.item.currency == 'usd':
                cur_name = "$"
                total_usd += p.qty * p.item.price
            elif p.item.currency == 'eur':
                cur_name = "€"
                total_eur += p.qty * p.item.price
            elif p.item.currency == 'rub':
                cur_name = "₽"
                total_rub += p.qty * p.item.price
            products.append(
                {
                    'id': p.item.pk,
                    'name': p.item.name,
                    'price': p.item.price,
                    'cur_name': cur_name,
                    'cur': p.item.currency,
                    'description': p.item.description,
                    'qty': p.qty,
                    'total': p.qty * p.item.price,
                }
            )

        cart_count = 0
        cart = Order.objects.all()

        for c in cart:
            cart_count += c.qty
        
        context = {
            'products': products,
            'cart_count': cart_count,
            'total_usd': total_usd,
            'total_eur': total_eur,
            'total_rub': total_rub,
        }
        
        return render(request, self.template_name, context=context)


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request, *args, **kwargs):
    print(kwargs)
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY

        price = stripe.Price.create(
            unit_amount=kwargs['price'] * 100,
            currency=kwargs['cur'],
            product= settings.PRODUCT,
        )['id']

        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price': price,
                        'quantity': kwargs['qty'],
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def add_to_cart(request, *args, **kwargs):

    if request.method == 'GET':
        try:
            order = Order(item=Item.objects.get(pk=int(request.GET['id'])), qty=int(request.GET['qty']))
            order.save()
        except django.db.utils.IntegrityError:
            product = Order.objects.get(item_id=int(request.GET['id']))
            product.qty += int(request.GET['qty'])
            product.save()

        return JsonResponse({"status": 'OK'}, status=200)

@csrf_exempt
def delete_product_to_cart(request, *args, **kwargs):

    if request.method == 'GET':
        product = Order.objects.get(item_id=int(request.GET['id']))
        product.delete()

        return JsonResponse({"status": 'OK', "qty": product.qty}, status=200)

@csrf_exempt
def delete_to_cart(request, *args, **kwargs):

    if request.method == 'GET':
        products = Order.objects.all()
        products.delete()

        return JsonResponse({"status": 'OK'}, status=200)