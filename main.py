import telebot
from TxtDatabase import DataBase

database = DataBase("data.txt")
bot = telebot.TeleBot("1824586460:AAGZ1WMqvKgInBdUgjaRFAiB70aX265X7zU")


@bot.message_handler(commands=["start"])
def add_to_database(message):
    if database.get_variable(f'{message.from_user.first_name} {message.from_user.last_name}') is None:
        database.new_variable(f'{message.from_user.first_name} {message.from_user.last_name}', "int",
                              message.from_user.id)
        print("this user are new")
    else:
        print("this user is in database")


bot.polling()
