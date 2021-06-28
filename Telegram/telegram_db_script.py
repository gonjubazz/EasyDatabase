import telebot
from TxtDatabase import DataBase

users_database = DataBase("telegram_users_db.txt")
messages_database = DataBase("telegram_messages_db.txt")

bot = telebot.TeleBot("1824586460:AAGZ1WMqvKgInBdUgjaRFAiB70aX265X7zU")


@bot.message_handler(content_types=["text"])
def add_to_database(message):
    if users_database.get_variable(f'{message.from_user.first_name} {message.from_user.last_name}') is None:
        users_database.new_variable(f'{message.from_user.first_name} {message.from_user.last_name}', "int",
                                    message.from_user.id)
        messages_database.new_variable(f'{message.from_user.first_name} {message.from_user.last_name}', "list",
                                       [message.text])
        print("New user!")
    else:
        messages_database.set_variable(f'{message.from_user.first_name} {message.from_user.last_name}', "list",
                                       messages_database.get_variable(
                                           f'{message.from_user.first_name} {message.from_user.last_name}').value + [
                                           message.text])


bot.polling()
