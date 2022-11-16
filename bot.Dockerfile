FROM tensorflow/tensorflow

RUN python3 -m pip install nltk pyTelegramBotAPI

RUN mkdir /project

COPY model_manager.py nlp_cleaner.py intents.json /project/

COPY main.py chatbot.py main_model.h5 /project/
WORKDIR /project

ENTRYPOINT python3 /project/main.py
