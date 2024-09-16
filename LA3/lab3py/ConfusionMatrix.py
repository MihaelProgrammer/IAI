def printAccuracy(predictions, testDataset):
    """
        Prints accuracy of ID3 model.
    @param predictions: predictions.
    @param testDataset: test dataset.
    """
    correct = 0

    for i in range(len(predictions)):
        if predictions[i] == testDataset[i][-1]:
            correct += 1

    print("[ACCURACY]:", "{0:.5f}".format(correct/len(predictions)))


def printPredictions(predictions):
    """
        Prints model predictions.
    @param predictions: predictions array.
    """
    print("[PREDICTIONS]: ", end="", sep="")
    for prediction in predictions:
        print(prediction, " ", end="", sep="")
    print()


def removeIndexes(array, indexes):
    """
        Removes indexed features from array.
    @param array: array.
    @param indexes: indexes to remove.
    @return: new array.
    """
    new_array = []

    for i in range(len(array)):
        if i in indexes:
            continue

        new_array.append(array[i])

    return new_array


def removeAll(array, element):
    """
        Removes all occurences of an element.
    @param array: array.
    @param element: element.
    @return: [new_array, indexes].
    """
    new_array = []
    indexes = []

    for i in range(len(array)):
        if array[i] == element:
            indexes.append(i)
        else:
            new_array.append(array[i])

    return [new_array, indexes]


def initConfusionMatrix(solutions):
    """
        Initializes confusion matrix.
    @param solutions: solutions.
    @return: confusion matrix.
    """
    solutionsList = sorted(set(solutions))
    confusionMatrix = []

    for i in range(len(solutionsList)):
        confusionMatrix.append([solutionsList[i]])
        for j in range(len(solutionsList)):
            confusionMatrix[i].append(0)

    return confusionMatrix


def getSolutionIndex(confusionMatrix, solution):
    """
        Gets index of a solution.
    @param confusionMatrix: confusion matrix.
    @param solution: solution.
    @return: index.
    """
    for i in range(len(confusionMatrix)):
        if confusionMatrix[i][0] == solution:
            return i

    return -1


def printConfusionMatrix(predictions, testDataset):
    """
        Prints confusion matrix.
    @param predictions: predictions.
    @param testDataset: test dataset.
    """
    solutions = []

    for i in range(len(testDataset)):
        solutions.append(testDataset[i][-1])

    confusionMatrix = initConfusionMatrix(solutions)

    for i in range(max(len(set(predictions)), len(set(solutions)))):
        currentSolution = confusionMatrix[i][0]

        for j in range(len(predictions)):
            if solutions[j] == currentSolution:
                if predictions[j] == currentSolution:
                    confusionMatrix[i][i + 1] += 1
                else:
                    index = getSolutionIndex(confusionMatrix, predictions[j])
                    if index != -1:
                        confusionMatrix[i][index + 1] += 1

    print("[CONFUSION_MATRIX]:")

    for i in range(len(confusionMatrix)):
        for j in range(len(confusionMatrix[i])):
            if j == 0:
                continue

            print(confusionMatrix[i][j], " ", end="", sep="")

        print()
