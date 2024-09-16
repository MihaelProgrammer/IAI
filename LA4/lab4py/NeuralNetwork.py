import numpy as np

from HelperFunctions import matrixSigmoid
from Neuron import Neuron


class NeuralNetwork:
    def __init__(self, architecture, inputSize, outputSize, neuralNetwork=None):
        """
            Initialize neural network.
        @param architecture: neural network architecture
        @param inputSize: size of input data
        @param outputSize: size of output data
        @param neuralNetwork: weights and biases for initialization
        """
        self.architecture = architecture

        temp = architecture.split("s")
        self.hiddenSize = int(temp[0])
        self.hiddenNum = len(temp) - 1
        self.inputSize = inputSize
        self.outputSize = outputSize

        self.neurons = []
        self.fitness = {}

        if neuralNetwork:
            self.initWeightsAndBiasesFromNeuralNetwork(neuralNetwork)
        else:
            self.initWeightsAndBiases()

    def initWeightsAndBiasesFromNeuralNetwork(self, neuralNetwork):
        """
            Method that handles initialization with given weights and biases.
        @param neuralNetwork: weights and biases
        """
        for i in range(len(neuralNetwork)):
            neuronLayer = []
            for j in range(len(neuralNetwork[i])):
                neuronLayer.append(Neuron(neuralNetwork[i][j][0], neuralNetwork[i][j][1]))

            self.neurons.append(neuronLayer)

    def initWeightsAndBiases(self):
        """
            Method that initializes weights and biases in case they were not provided.
        """
        neuronLayer = []
        for j in range(self.hiddenSize):
            neuronLayer.append(Neuron(np.random.normal(0, 0.01, self.inputSize), 0))

        self.neurons.append(neuronLayer)

        for i in range(self.hiddenNum - 1):
            neuronLayer = []
            for j in range(self.hiddenSize):
                neuronLayer.append(Neuron(np.random.normal(0, 0.01), 0))

            self.neurons.append(neuronLayer)

        self.neurons.append([Neuron(np.random.normal(0, 0.01, self.hiddenSize), 0)])

    def forward(self, inputs, outputs):
        """
            Method that forwards input through neural network to get output.
        @param inputs: input data
        @param outputs: output data
        @return: calculated output
        """
        output = []
        for neuronLayer in self.neurons[:-1]:
            hiddenOutput = []
            for neuron in neuronLayer:
                hiddenOutput.append(neuron.forward(inputs)[0])
            output.append(matrixSigmoid(hiddenOutput))

        lastHiddenOutput = output[-1]
        for outputNeuron in self.neurons[-1]:
            output.append(outputNeuron.forward(lastHiddenOutput))

        if type(output[-1]) is np.ndarray or type(output[-1]) is list:
            myOutput = output[-1][0]
        else:
            myOutput = output[-1]
        self.adjustFitness(outputs, myOutput)

        return myOutput

    def adjustFitness(self, output, myOutput):
        """
            Method that calculates fitness of neural network after each iteration.
        @param output: actual output
        @param myOutput: neural network output
        """
        difference = myOutput - output
        diffSquared = difference * difference

        if len(self.fitness) == 0:
            self.fitness = {
                "diffSquaredSum":   diffSquared,
                "iterations":       1,
            }

        else:
            self.fitness["diffSquaredSum"] = self.fitness["diffSquaredSum"] + diffSquared
            self.fitness["iterations"] = self.fitness["iterations"] + 1

    def getFitness(self):
        """
            Returns fitness of neural network
        @return: fitness or "undefined" if no inputs have been forwarded
        """
        if len(self.fitness) == 0:
            return "Undefined"

        return 1 / (self.fitness["diffSquaredSum"] / self.fitness["iterations"])

    def getIterationNumber(self):
        """
            Returns how much data has been forwarded.
        @return: Number of forwarded inputs
        """
        return self.fitness["iterations"]

    def getError(self):
        """
            Returns sum of squared differences of network output and actual output
        @return:
        """
        if len(self.fitness) == 0:
            return "Undefined"

        return self.fitness["diffSquaredSum"] / self.fitness["iterations"]

    def getNeurons(self):
        """
            Returns layers of neurons.
        @return: neurons sorted into layers.
        """
        return self.neurons

    def __str__(self):
        """
            Creates a string to represent neural network.
        @return: string
        """
        string = ""
        for i in range(len(self.neurons)):
            if i == len(self.neurons) - 1:
                string = string + "Output layer:\n"
            else:
                string = string + str(i + 1) + ". layer:\n"
            for neuron in self.neurons[i]:
                string = string + "\t" + str(neuron) + ",\n"

        return string
