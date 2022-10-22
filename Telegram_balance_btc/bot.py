import config
from Telegram_balance_btc import get_data_price
import telebot
from telebot import types

"""Создаем объект бота и передаем токен"""
bot = telebot.TeleBot(token = config.token)

"""Обрабатываем команду start"""
@bot.message_handler(commands=['start'])
def get_price(message):
    bot.send_message(message.chat.id, "Hello, \n I am bot, \n I can see the current prices for bitcoin on exchanges and show them to you \n all my commands: \n    1. /start \n    2. /button")

"""Обрабатываем команду button"""
@bot.message_handler(commands=['button'])
def button(message):
    """Создаем объект клавиатуры"""
    markup = types.ReplyKeyboardMarkup()
    """Создаем кнопку"""
    button_1_text = types.KeyboardButton("update price")
    """Добавляем кнопку в клавиатуру"""
    markup.add(button_1_text)
    """При нажатии на команду button будет выведено приглашение воспользоваться кнопкой"""
    bot.send_message(message.chat.id, "click here if need update", reply_markup=markup)

"""Обрабатываем остальной текст"""
@bot.message_handler(content_types=['text'])
def get_price(message):
    """Проверяем, если пользователь ввел текст или воспользовался кнопкой, заходим в блок"""
    if message.text == "update price":
        """Сообщаем, что команда принята и запустился процесс загрузки цен"""
        bot.send_message(message.chat.id, "Application accepted, please wait")
        """Создаем объект класса Price что бы вытянуть данные по ценам"""
        price_obj = get_data_price.Price()
        price_dict = price_obj.get_data()
        """Добавляем к текстовому описанию проблеы, для красового отображения результата"""
        for key, val in price_dict.items():
            if key == "BTC(GateIO)":
                tmp_key = "BTC(GateIO)  "
            elif key == "BTC(FTX)":
                tmp_key = "BTC(FTX)       "
            else:
                tmp_key = key
            """Выводим на экран полученный результат"""
            bot.send_message(message.chat.id, f'{tmp_key} : {val}')
        """Оповещаем пользхователя о завершении выполнения команды"""
        bot.send_message(message.chat.id, "Done!")
    else:
        """Обработка введенного сообщения не предусмотрена"""
        bot.send_message(message.chat.id, "I don't know this command.")

def main():
    bot.infinity_polling()

if __name__ == '__main__':
    main()