from random import choice
from re import sub as replace_all

import numpy as np
import telebot

import model_manager
import nlp_cleaner

ERROR_THRESHOLD = 0.1
bot = telebot.TeleBot('i_wont_give_you_my_token', parse_mode='MarkdownV2')

if __name__ == '__main__':
    print('Loading the model...', flush=True)
    model = model_manager.load_model('main_model')
    print('Reading responses...', flush=True)
    intents = model_manager.load_intents()
    usable_tokens, classes = model_manager.prepare_predict_data()


def predict_class(message):
    p = bag_of_words(message)
    res = model.predict(np.array([p]))[0]
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda z: z[1], reverse=True)
    processed_tags = []
    for r in results:
        processed_tags.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return processed_tags


def bag_of_words(message):
    sentence_words = nlp_cleaner.clean_up_sentence(message)
    bag = []

    for token in usable_tokens:
        bag.append(1 if token in sentence_words else 0)

    return np.array(bag)


def get_response(predicted_tag):
    tag = predicted_tag['intent']
    intent_list = intents['intents']

    for intent in intent_list:
        if intent['tag'] == tag:
            return choice(intent['responses'])
    return None


welcome_text = """
***Привет\\!*** Я очень умный бот, с которым _интересно_ поговорить
Используй /help для того, чтобы узнать, что я могу
"""
help_text = """
Что я умею:
\\* Все сообщения, которые ты мне пишешь, я читаю и, используя свои ~бесконечные~ возможности, отвечаю на них
\\* Используй /start для того, чтобы я мог с тобой общаться
\\* Используй /help для того, чтобы узнать, что я могу
"""
class_error_text = """
||Я не понял\\!||
"""


@bot.message_handler(commands=['start'])
def start_request(message):
    bot.reply_to(message, welcome_text)


@bot.message_handler(commands=['help'])
def help_request(message):
    bot.reply_to(message, help_text)


@bot.message_handler(content_types=['text'])
def plain_text(message):
    message_text = message.text
    message_class = predict_class(message_text)
    message_response = get_response(message_class[0])

    if message_response:
        message_response = replace_all(r'([_`*[])', r'\\\1', message_response)
        bot.reply_to(message, message_response, parse_mode="Markdown")
    else:
        bot.reply_to(message, class_error_text)


if __name__ == '__main__':
    print('Start long-polling...', flush=True)
    bot.infinity_polling(allowed_updates=["message"])
