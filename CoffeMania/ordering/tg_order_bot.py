import telebot


def send_order_tg(bot_token, chatid, message):
    bot = telebot.TeleBot(bot_token)
    bot.send_message(chatid, message)
