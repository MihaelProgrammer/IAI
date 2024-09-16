import sys

from DataLoader import getData
from GenerationGeneticAlgorithm import geneticAlgorithm


def main():
    """
        Main function. Handles reading and forwarding data from terminal.
    """
    args = sys.argv[1:]

    common = "D:\\Vaks\\uui\\2023\\autograder\\data\\lab4\\files\\"

    trainContent = getData(common + args[args.index("--train") + 1])
    trainContent.pop(0)
    testContent = getData(common + args[args.index("--test") + 1])
    testContent.pop(0)
    architecture = args[args.index("--nn") + 1]
    populationSize = int(args[args.index("--popsize") + 1])
    elitism = int(args[args.index("--elitism") + 1])
    mutationProbability = float(args[args.index("--p") + 1])
    noiseDeviation = float(args[args.index("--K") + 1])
    iterationNumber = int(args[args.index("--iter") + 1])

    geneticAlgorithm(trainContent, testContent, architecture, populationSize, elitism,
                     mutationProbability, noiseDeviation, iterationNumber)


if __name__ == "__main__":
    main()
