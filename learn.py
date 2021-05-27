from tensorflow.keras.losses import mean_absolute_error
from degrade_data import generator_low_and_high_sound
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.layers import Dense
from download_data import getFileIterator
import numpy as np

model = Sequential()
model.add(Dense(1000, input_dim=980, activation="sigmoid"))
model.add(Dense(1000, activation="sigmoid"))
model.add(Dense(1000, activation="sigmoid"))
model.compile(
    optimizer = SGD(learning_rate=0.01, momentum=0.0, nesterov=False),
    metrics = ["accuracy"],
    loss = mean_absolute_error)

X = []
Y = []
for path in getFileIterator():
    for (x, y) in generator_low_and_high_sound(path):
        if len(x[0]) != 980:
            x[0].extend([0.0] * (980 - len(x[0])))
        if len(y[0]) != 1000:
            y[0].extend([0.0] * (1000 - len(y[0])))
        if X is None:
            X = x
        else:
            X.append(x[0])
        if Y is None:
            Y = y
        else:
            Y.append(y[0])
        print('\r{:.2%} '.format(len(X) / 100000.), end='', flush=True)
        if len(X) >= 100000:
            print()
            model.fit(np.array(X), np.array(Y), epochs=1000, validation_split=0.1, verbose=1)
            X = []
            Y = []
    print()
