from json import load as read_json_source

from tensorflow.keras.models import load_model as load_keras_model

import nlp_cleaner


def save_model(model, model_name=None):
    if model_name is None:
        model_name = "model_with_no_future"
    model.save(f"{model_name}.h5")


def load_model(model_name=None):
    if model_name is None:
        model_name = "model_with_no_future"
    return load_keras_model(f'{model_name}.h5')


def load_intents():
    with open("intents.json", encoding="utf-8") as f:
        return read_json_source(f)


def prepare_train_data():
    intents = load_intents()

    token_list = []
    train_data = []
    class_list = []

    for intent in intents['intents']:
        for example in intent['examples']:
            tokens = nlp_cleaner.tokenize(example)

            token_list.extend(tokens)
            train_data.append((tokens, intent['tag']))

            if intent['tag'] not in class_list:
                class_list.append(intent['tag'])

    token_list = nlp_cleaner.clean_up_tokens(token_list)

    token_list = sorted(set(token_list))
    class_list = sorted(set(class_list))

    return token_list, class_list, train_data


def prepare_predict_data():
    token_list, class_list, train_data = prepare_train_data()
    return token_list, class_list
