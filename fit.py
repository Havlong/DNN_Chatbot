from random import shuffle

import numpy as np
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.optimizers import SGD

import model_manager
import nlp_cleaner

intents = model_manager.load_intents()

token_list, class_list, train_data = model_manager.prepare_train_data()

training = []
output_empty = [0 for i in range(len(class_list))]

for (tokens, predicted_class) in train_data:
    bag = []
    tokens = [nlp_cleaner.process_token(x) for x in tokens]

    for token in token_list:
        bag.append(1 if token in tokens else 0)

    output_row = list(output_empty)
    output_row[class_list.index(predicted_class)] = 1
    training.append([bag, output_row])

shuffle(training)
training = np.array(training, dtype=object)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

history = model.fit(np.array(train_x), np.array(train_y), epochs=100, batch_size=5, verbose=1)

model_manager.save_model(model, 'main_model')
