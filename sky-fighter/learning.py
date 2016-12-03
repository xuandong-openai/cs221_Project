from agent import getFeatureVector
from collections import Counter
import pickle


class TDLearner:
    def __init__(self):
        self.weight = Counter()
        self.eta = 0.1
        self.gama = 1

    def loadWeightFromFile(self):
        with open('weight.txt', 'rb') as handle:
            return pickle.loads(handle.read())
        # with open('weight.txt') as f:
        #     for line in f:
        #         res.append(float(line))

    def dot(self, feature, weight):
        res = 0
        for key in feature:
            res += feature[key] * weight[key]
        return res

    def scale(self, scale, dict):
        for key in dict:
            dict[key] *= scale
        return dict

    def updateWeight(self, currGameState, nextGameState, reward):
        prediction = self.dot(self.weight, getFeatureVector(currGameState))
        target = reward + self.gama * self.dot(self.weight, getFeatureVector(nextGameState))
        derivative = getFeatureVector(currGameState)
        self.weight = self.scale(self.eta * (prediction - target), derivative)

    def writeWeightToFile(self):
        with open('file.txt', 'wb') as handle:
            pickle.dump(self.weight, handle)
        # with open('weight', 'w') as f:
        #     for w in self.weight:
        #         f.write(str(w) + '\n')

    def getWeight(self):
        return self.weight
