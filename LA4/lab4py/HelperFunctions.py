import numpy as np


def sigmoid(x):
    """
        Calculates sigmoid function for given value.
    @param x: value
    @return: sigmoid(x)
    """
    return 1 / (1 + np.exp(-x))


def matrixSigmoid(matrix):
    """
        Calculates sigmoid value for each element in given matrix
    @param matrix: starting matrix
    @return: matrix of sigmoid values
    """
    newMatrix = []

    for element in matrix:
        newMatrix.append(sigmoid(element))

    return newMatrix


def getAverage(values):
    """
        Calculates average value from array.
    @param values: array of values
    @return: average
    """
    return sum(values) / len(values)


def loadWB(neuralNetwork):
    """
        Creates an array of weights and biases from neural network.
    @param neuralNetwork: neural network
    @return: arrays of neuron weights and biases sorted through layers.
    """
    networkWB = []

    for neuronLayer in neuralNetwork.getNeurons():
        layerWB = []
        for neuron in neuronLayer:
            layerWB.append([neuron.getWeight(), neuron.getBias()])

        networkWB.append(layerWB)

    return networkWB
