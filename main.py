from random import choice

import numpy as np

import model_manager
import nlp_cleaner
from chatbot import bot

ERROR_THRESHOLD = 0.1

if __name__ == '__main__':
    model = model_manager.load_model('main_model')
    intents = model_manager.load_intents()
    usable_tokens, classes = model_manager.prepare_predict_data()
    bot.infinity_polling()


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

    return "||Я не понял!||"


@bot.message_handler(func=lambda x: True)
def plain_text(message):
    message_text = message.text
    message_class = predict_class(message_text)
    message_response = get_response(message_class)
    bot.reply_to(message, message_response)
