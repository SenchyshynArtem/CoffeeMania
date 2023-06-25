from django.shortcuts import render
from .models import ProductInBasket
from django.http import JsonResponse
from ordering.views import is_user_registered

def show_basket(request):
    session_key = request.session.session_key
    if is_user_registered(session_key):  # Перевірка, чи є користувач зареєстрованим
        user = is_user_registered(session_key)  # Отримання зареєстрованого користувача
        products_in_basket = ProductInBasket.objects.filter(user=user)  # Фільтрування продуктів в кошику для даного користувача
    else:
        products_in_basket = ProductInBasket.objects.filter(session_key=session_key)  # Фільтрування продуктів в кошику за сесією
    # Обчислення вартості продуктів у кошику
    for product_in_basket in products_in_basket:
        product_in_basket.products_price = int(product_in_basket.product.price) * int(product_in_basket.amount)
        product_in_basket.save()

    full_price = 0  # Загальна вартість кошика

    for product_in_basket in products_in_basket:
        full_price += int(product_in_basket.products_price)  # Підрахунок загальної вартості

    return render(request, 'basket/basket.html', context={'products_in_basket': products_in_basket, "full_price": full_price})


def delete_from_basket(request):
    product_id = request.POST.get('pk_product')  # Отримання ідентифікатора продукту, який потрібно видалити з кошика
    ProductInBasket.objects.get(pk=product_id).delete()  # Видалення продукту з кошика
    return JsonResponse({})  # Повернення пустої відповіді


def change_amount(request):
    operation = request.POST.get('operation')  # Отримання операції зміни кількості продукту (збільшення або зменшення)
    product = ProductInBasket.objects.get(pk=request.POST.get('product_pk'))  # Отримання продукту в кошику

    if product.amount + int(operation) <= 0:
        product.amount = 1  # Зміна кількості на мінімальне значення, якщо кількість стає від'ємною або нульовою

    elif product.amount + int(operation) >= 99:
        product.amount = 99  # Зміна кількості на максимальне значення, якщо кількість стає більшою за 99

    else:
        product.amount = product.amount + int(operation)  # Збільшення або зменшення кількості продукту
    product.products_price = product.amount * int(product.product.price)
    product.save()  # Збереження змін  

    return JsonResponse({})  # Повернення пустої відповіді


def update_basket_counter(request):
    session_key = request.session.session_key
    if is_user_registered(session_key):  # Перевірка, чи є користувач зареєстрованим
        user = is_user_registered(session_key)  # Отримання зареєстрованого користувача
        products_in_basket = len(ProductInBasket.objects.filter(user=user))  # Кількість продуктів в кошику для даного користувача
    else:
        products_in_basket = len(ProductInBasket.objects.filter(session_key=session_key))  # Кількість продуктів в кошику за сесією

    return JsonResponse({'count_product': products_in_basket})  # Повернення кількості продуктів у кошику у відповіді JSON
