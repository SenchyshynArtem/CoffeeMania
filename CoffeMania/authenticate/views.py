from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from basket.models import ProductInBasket
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .models import *


def show_registration(request):
    # Отображение страницы регистрации
    return render(request, "auth/reg.html")


def show_login(request):
    # Отображение страницы входа
    return render(request, "auth/login.html")


def register_user(request):
    # Регистрация пользователя
    response = {}
    user_data = request.POST

    # Проверка на разрешенные символы в полях firstname и name
    firstname = user_data['firstname']
    name = user_data['name']
    if not firstname.isalpha() or not name.isalpha():
        response['error'] = "Ім'я та прізвище повинні містити тільки літери!"
        return JsonResponse(response)

    # Проверка на совпадение паролей
    password = user_data['password']
    confirm_password = user_data['confirm_password']
    if password != confirm_password:
        response['error'] = 'Пароли не совпадают'
        return JsonResponse(response)

    # Переменная для хранения продуктов в корзине
    products_in_basket = None
    response['access'] = ''

    try:
        session_key = request.session.session_key
        if session_key:
            # Получение продуктов в корзине для текущего сеанса
            products_in_basket = ProductInBasket.objects.filter(
                session_key=session_key)

        # Создание и сохранение нового пользователя
        user = User.objects.create_user(first_name=(
            firstname + ' ' + name), username=user_data['phone'], password=password)
        user.save()

        if products_in_basket:
            # Обновление продуктов в корзине, чтобы привязать их к новому пользователю
            products_in_basket.update(session_key='', user=user)

        # Авторизация пользователя после успешной регистрации
        login(request, user)
        response['access'] = 'available'

    except IntegrityError:
        response['error'] = "Такий користувач вже існує"

    return JsonResponse(response)


def login_user(request):
    # Вход пользователя
    response = {}

    user_data = request.POST
    user = authenticate(
        request, username=user_data['phone'], password=user_data['password'])

    if user:
        response['error'] = ''
        response['access'] = 'available'
        login(request, user)
    else:
        response['access'] = ''
        response['error'] = 'Номер телефону або пароль не вірні'

    return JsonResponse(response)
