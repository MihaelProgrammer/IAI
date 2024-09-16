import numpy as np

from NeuralNetwork import NeuralNetwork

from HelperFunctions import loadWB, getAverage


def elitismSelection(generation, elitismFactor):
    """
        Function that returns array containing units from generation with best fitness.
    @param generation: generation of units
    @param elitismFactor: number of best units to return
    @return: array of elitismFactor best units from generation
    """
    desc = sorted(generation, key=lambda x: x.getFitness(), reverse=True)

    return desc[:elitismFactor]


def applyMutation(networkWB, kFactor, probability):
    """
        Function that applies gaussian noise to networks weights and biases.
    @param networkWB: network weights and biases
    @param kFactor: gaussian noise deviation
    @param probability: probability that noise will be applied
    @return:
    """
    newNetworkWB = []

    for neuronLayer in networkWB:
        kVector = []
        for i in range(2):
            kWB = []
            for j in range(len(neuronLayer)):
                if type(neuronLayer[j][i]) is np.ndarray or type(neuronLayer[j][i]) is list:
                    kWB_ = []
                    for _ in neuronLayer[j][0]:
                        if np.random.random() <= probability:
                            kWB_.append(np.random.normal(0, kFactor))
                        else:
                            kWB_.append(0)
                    kWB.append(kWB_)

                else:
                    if np.random.random() <= probability:
                        kWB.append(np.random.normal(0, kFactor))
                    else:
                        kWB.append(0)

            kVector.append(kWB)

        for i in range(len(neuronLayer)):
            if type(neuronLayer[i][0]) is np.ndarray or type(neuronLayer[i][0]) is list:
                for j in range(len(neuronLayer[i][0])):
                    neuronLayer[i][0][j] += kVector[0][i][j]
            else:
                neuronLayer[i][0] += kVector[0][i]
            neuronLayer[i][1] += kVector[1][i]

        newNetworkWB.append(neuronLayer)

    return newNetworkWB


def crossover(network1, network2, kFactor, probability):
    """
        Function that returns a child from 2 parents.
    @param network1: first parent
    @param network2: second parent
    @param kFactor: noise deviation
    @param probability: probability noise will be applied
    @return: child
    """
    network1WB = loadWB(network1)
    network2WB = loadWB(network2)

    newNetworkWB = []
    for i in range(len(network1WB)):
        layerWB = []
        for j in range(len(network1WB[i])):
            if type(network1WB[i][j][0]) is np.ndarray or type(network1WB[i][j][0]) is list:
                weights = []
                for k in range(len(network1WB[i][j][0])):
                    weights.append(getAverage([network1WB[i][j][0][k], network2WB[i][j][0][k]]))

                layerWB.append([weights, getAverage([network1WB[i][j][1], network2WB[i][j][1]])])
            else:
                layerWB.append([getAverage([network1WB[i][j][0], network2WB[i][j][0]]),
                                getAverage([network1WB[i][j][1], network2WB[i][j][1]])])

        newNetworkWB.append(layerWB)

    newNetworkWB = applyMutation(newNetworkWB, kFactor, probability)

    return NeuralNetwork(network1.architecture, network1.inputSize, network1.outputSize, neuralNetwork=newNetworkWB)


def trainError(generation, iteration):
    """
        Function that writes error for given iteration to standard output.
    @param generation: generation of units
    @param iteration: current iteration
    """
    bestUnit = elitismSelection(generation, 1)[0]
    print("[Train error @", iteration, "]: ", bestUnit.getError(), sep="")


def geneticAlgorithm(trainContent, testContent, architecture, popSize, elitism, probability, kFactor, iterations):
    """
        Function that applies genetic algorithm.
    @param trainContent: training data
    @param testContent: testing data
    @param architecture: neural network architecture
    @param popSize: population size
    @param elitism: number of best units to be forwarded to next generation
    @param probability: probability of applying noise
    @param kFactor: noise deviation
    @param iterations: number of iterations
    """
    generation = []
    inputSize = len(trainContent[0]) - 1
    outputSize = 1

    for i in range(popSize):
        generation.append(NeuralNetwork(architecture, inputSize, outputSize))

    for i in range(iterations):
        for unit in generation:
            for index in range(len(trainContent)):
                unit.forward(trainContent[index][:-1], trainContent[index][-1])

        if (i + 1) % 2000 == 0:
            trainError(generation, i + 1)

        parents = elitismSelection(generation, 2)
        child = crossover(parents[0], parents[1], kFactor, probability)

        newGeneration = elitismSelection(generation, elitism)
        newGeneration.append(child)

        while len(newGeneration) < popSize:
            newGeneration.append(NeuralNetwork(architecture, inputSize, outputSize))

        generation = newGeneration

    bestUnit = generation[0]

    bestUnit.fitness = {}

    for index in range(len(testContent)):
        bestUnit.forward(testContent[index][:-1], testContent[index][-1])

    print("[Test error]: ", bestUnit.getError(), sep="")
