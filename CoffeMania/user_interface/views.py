from django.shortcuts import render
from ordering.tg_order_bot import send_order_tg
from coffeemania.settings import TELEGRAM_CHAT_ID, TELEGRAM_BOT_TOKEN

# Create your views here.


def show_contact_page(request):
    if request.method == "POST":
        req = request.POST
        message = f'📝Повідомлення: {req["message"]} \n\n👤Клієнт: {req["name"]}\n📞Номер телефону: {req["phone"]}'
        send_order_tg(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)
    return render(request, "user_interface/contact_page.html")


def show_main_page(request):
    return render(request, "user_interface/main_page.html")
