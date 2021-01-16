import numpy as np 
import pandas as pd 
import tensorflow as tf
from preprocessing import Preprocessing

trainingData = pd.read_excel("./data/training.xlsx", engine = "openpyxl")
testingData = pd.read_excel("./data/testing.xlsx", engine = "openpyxl")

trainingData = trainingData[["new_cases"]]
testingData = testingData[["new_cases"]]

process = Preprocessing(trainingData, testingData)

xTrain, yTrain = process.Structure(7)
xTest, yTest = process.Structure(7, training = False)

units = 50
dropout = 0.25


## DEFINING THE MODEL ##

model = tf.keras.models.Sequential()

model.add(tf.keras.layers.LSTM(units = units, return_sequence = True, input_shape = (xTrain.shape[1], 1)))
model.add(tf.keras.layers.Dropout(dropout))

model.add(tf.keras.layers.LSTM(units = units, return_sequence = True))
model.add(tf.keras.layers.Dropout(dropout))

model.add(tf.keras.layers.LSTM(units = units, return_sequence = True))
model.add(tf.keras.layers.Dropout(dropout))

model.add(tf.keras.layers.LSTM(units = units))
model.add(tf.keras.layers.Dropout(dropout))

model.add(tf.keras.layers.Dense(units = 1))

model.compile(optimizer = "adam", loss = "mean_sqared_error")
model.fit(x = xTrain, y = yTrain, epochs = 100, validation_data = (xTest, yTest), callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor = "val_loss",
        patience = 5,
        verbose = 2,
        mode = "min",
        restore_best_weights = True)])



