FROM tensorflow/tensorflow

RUN python3 -m pip install nltk pyTelegramBotAPI

RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader wordnet
RUN python3 -m nltk.downloader omw-1.4

RUN mkdir /project

COPY model_manager.py nlp_cleaner.py intents.json /project/

COPY main.py main_model.h5 /project/
WORKDIR /project

ENTRYPOINT python3 /project/main.py
