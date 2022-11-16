import telebot

bot = telebot.TeleBot('i_wont_give_you_my_token', parse_mode='MARKDOWN')

welcome_text = """
***Привет!*** Я очень умный бот, с которым _интересно_ поговорить
Используй `/help` для того, чтобы узнать, что я могу
"""

help_text = """
Что я умею:
- Все сообщения, которые ты мне пишешь, я читаю и, используя свои ~~бесконечные~~ возможности, отвечаю на них
- Используй `/start` для того, чтобы я мог с тобой общаться
- Используй `/help` для того, чтобы узнать, что я могу
"""


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, welcome_text)


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, help_text)
