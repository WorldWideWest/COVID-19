import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class Preprocessing:

    def __init__(self, trainingData, testingData):
        self.trainingData = trainingData
        self.testingData = testingData

    def Structure(self, lookback, training = True):
        if training:
            data = self.trainingData.values
            scaler = MinMaxScaler(feature_range = (-1, 1))
            data = scaler.fit_transform(data.reshape(-1, 1))

            xTrain, yTrain = [], []

            for i in range(lookback, data.shape[0]):
                xTrain.append(data[i - lookback : i, 0])
                yTrain.append(data[i, 0])
            
            xTrain, yTrain = np.array(xTrain), np.array(yTrain)
            xTrain = np.reshape(xTrain, (xTrain.shape[0], xTrain.shape[1], 1))

            return [xTrain, yTrain]
        else:
            totalData = pd.concat((self.trainingData, self.testingData), axis = 0)
            inputs = totalData[len(totalData) - len(self.testingData) - lookback : ].values
            scaler = MinMaxScaler(feature_range = (-1, 1))
            inputs = scaler.fit_transform(inputs.reshape(-1, 1))

            xTest, yTest = [], []
            
            for i in range(lookback, lookback + len(self.testingData)):
                xTest.append(inputs[i - lookback : i, 0])
                yTest.append(inputs[i, 0])

            xTest, yTest = np.array(xTest), np.array(yTest)
            xTest = np.reshape(xTest, (xTest.shape[0], xTest.shape[1], 1))

            return [xTest, yTest]
 
