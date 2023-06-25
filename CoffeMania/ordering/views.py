from django.shortcuts import render
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from .tg_order_bot import send_order_tg
from basket.models import ProductInBasket
from coffeemania.settings import TELEGRAM_CHAT_ID, TELEGRAM_BOT_TOKEN
from .models import Orders

# Create your views here.


def is_user_registered(session_key):
    try:
        session = Session.objects.get(session_key=session_key)
        user_id = session.get_decoded().get("_auth_user_id")
        user = User.objects.filter(pk=user_id).first()
        return user
    except Session.DoesNotExist:
        return None


def ordering(request):
    context = {}
    """'name': ['Ярослав'], 'surname': ['Турчин'], 'phone': ['+(380) 96-991-3414'],
    'street': ['Калинова'], 'build': ['41'], 'room': ['']"""
    session_key = request.session.session_key
    if is_user_registered(session_key):
        user = is_user_registered(session_key)
        fullname_user = user.first_name.split(" ")
        adress_user = user.last_name.split(" ")
        context["name"] = fullname_user[1]
        context["surname"] = fullname_user[0]
        if adress_user:
            if len(adress_user) == 3:
                context["street"] = adress_user[0]
                context["house"] = adress_user[1]
                context["room"] = adress_user[2]
            elif len(adress_user) == 2:
                context["street"] = adress_user[0]
                context["house"] = adress_user[1]
                context["room"] = ""
            elif len(adress_user) == 1:
                context["street"] = adress_user[0]
                context["house"] = ""
                context["room"] = ""

        context["products"] = ProductInBasket.objects.filter(user=user)
    else:
        context["products"] = ProductInBasket.objects.filter(session_key=session_key)

    if request.method == "POST":
        order_numb = len(Orders.objects.all()) + 1
        fullprice = 0
        order = f'Замовлення #{order_numb}\n\n👤Клієнт: {request.POST["surname"] + " " + request.POST["name"]}\n📞Номер телефону: {request.POST["phone"]}\n🏡Адреса: вул. {request.POST["street"]}, буд. {request.POST["build"]}, кв. {request.POST["room"]}\n\n📝Лист замовлення:\n'
        for product_from_basket in context["products"]:
            order += f"- «{product_from_basket.product.name}» | {product_from_basket.amount}шт({product_from_basket.products_price}₴);\n"
            fullprice += product_from_basket.products_price
        order += f"Всього: {fullprice}₴"
        send_order_tg(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, order)
        if is_user_registered(session_key):
            Orders.objects.create(
                session_key=None, user=is_user_registered(session_key), order=order
            )
            ProductInBasket.objects.filter(
                user=is_user_registered(session_key)
            ).delete()
        else:
            Orders.objects.create(session_key=session_key, user=None, order=order)
            ProductInBasket.objects.filter(session_key=session_key).delete()

    return render(request, "ordering/ordering.html", context)
