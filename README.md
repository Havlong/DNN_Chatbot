# DNN_Chatbot

Simple DNN chatbot for Telegram

Language used:

- Python 3.9

Libraries used:

- `TeleBot`
- `TensorFlow Keras`
- `NLTK`

Be sure to install required libs: ```python3 -m pip install tensorflow nltk pyTelegramBotAPI ```

## To fit the model

- launch `python3 fit.py` and it will fit model and save it to `main_model.h5`
- Using Docker
    - `docker build -f fit.Dockerfile -t dnn_fit .`
    - `docker run -d --name chatbot_dnn dnn_fit`
    - `docker cp chatbot_dnn:/project/main_model.h5 ./`
    - `docker rm chatbot_dnn`

## To start bot

- launch `python3 main.py` and it will start long-polling messages for Bot
- Using Docker
    - `docker build -f bot.Dockerfile -t dnn_bot .`
    - `docker run -d --rm dnn_bot`

Big thanks for the help to **_NeuralNine_** and his [Repository](https://github.com/NeuralNine/neuralintents)
