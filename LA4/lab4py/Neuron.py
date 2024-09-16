import numpy as np


class Neuron:
    def __init__(self, weights, bias):
        """
            Initialize neuron.
        @param weights: single value or array of values that represent weights of a neuron
        @param bias: neuron bias
        """
        if type(weights) is np.ndarray or type(weights) is list:
            self.weights = np.reshape(weights, (len(weights), 1))
        else:
            self.weights = weights

        self.bias = bias

    def adjustWeight(self, newWeights):
        """
            Changes weight value.
        @param newWeights: new value(s)
        """
        if type(newWeights) is np.ndarray or type(newWeights) is list:
            self.weights = np.reshape(newWeights, (len(newWeights), 1))
        else:
            self.weights = newWeights

    def adjustBias(self, newBias):
        """
            Changes bias value.
        @param newBias: new value
        """
        self.bias = newBias

    def getWeight(self):
        """
            Returns weight(s) of neuron.
        @return: array or single value of weight
        """
        if type(self.weights) is np.ndarray or type(self.weights) is list:
            return np.reshape(self.weights, (len(self.weights),))

        return self.weights

    def getBias(self):
        """
            Returns bias of neuron.
        @return: single value neuron bias
        """
        return self.bias

    def forward(self, inputs):
        """
            Calculates neurons output for given input data.
        @param inputs: input data
        @return: neurons output data
        """
        if type(inputs) is np.ndarray or type(inputs) is list:
            return np.dot(inputs, self.weights) + self.bias
        else:
            return [inputs * self.weights + self.bias]

    def __str__(self):
        """
            Returns a string representation of neurons weight and bias.
        @return: string
        """
        return "weights: " + str(self.weights) + ", bias: " + str(self.bias)
