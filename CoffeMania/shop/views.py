from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from basket.models import ProductInBasket


def show_shop(request):
    # Получаем все продукты из базы данных
    all_products = Product.objects.all()
    return render(request, 'shop/shop.html', context={'all_products': all_products})


def show_product(request, product_pk):
    if request.method == 'POST':
        # Получаем ключ сеанса пользователя
        session_key = request.session.session_key
        # Получаем объект продукта по его primary key (pk)
        product = Product.objects.get(pk=product_pk)
        amount = int(request.POST['amount'])
        if session_key:
            try:
                # Получаем сеанс пользователя
                session = Session.objects.get(
                    session_key=request.session.session_key)
                # Получаем идентификатор пользователя из сеанса
                user_id = session.get_decoded().get('_auth_user_id')

                try:
                    # Пытаемся найти объект ProductInBasket для пользователя и продукта
                    product = ProductInBasket.objects.get(user=User.objects.get(id=user_id), product=product)
                    product.amount += amount
                    product.save()
                except:
                    # Если объект ProductInBasket не найден, создаем новый для пользователя и продукта
                    ProductInBasket.objects.create(session_key='', user=User.objects.get(id=user_id), product=product, amount=amount, )
            except:
                try:
                    # Пытаемся найти объект ProductInBasket для сеанса пользователя и продукта
                    product = ProductInBasket.objects.get(session_key=session_key, product=product)
                    product.amount += amount
                    product.save()
                except:
                    # Если объект ProductInBasket не найден, создаем новый для сеанса пользователя и продукта
                    ProductInBasket.objects.create(session_key=session_key, product=product, amount=amount)
        else:
            # Если ключ сеанса не существует, создаем новый ключ и объект ProductInBasket
            request.session.cycle_key()
            session_key = request.session.session_key
            ProductInBasket.objects.create(session_key=session_key, product=product, amount=amount)

    # Получаем объект продукта для отображения
    product = get_object_or_404(Product, pk=product_pk)

    return render(request, 'product/product.html', context={'product': product})
