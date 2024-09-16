import math
import DecisionTree as tree


def getAllValues(subtree, values):
    if type(subtree) is tree.Leaf:
        value = subtree.getValue()
        if value in values.keys():
            values[str(value)] += 1
        else:
            values[str(value)] = 1
    elif type(subtree) is tree.Node:
        getAllValues(subtree.getSubtree(), values)
    elif type(subtree[0]) is not list:
        if subtree[0] in values.keys():
            values[str(subtree[0])] += 1
        else:
            values[str(subtree[0])] = 1
        getAllValues(subtree[1], values)
    else:
        for subset in subtree:
            getAllValues(subset, values)

    return values


def findTrimmedLabel(trainingDataset, value, parentFeature, allFeatures):
    index = allFeatures.index(parentFeature)

    newDataset = datasetSorter(trainingDataset, index)
    subset = []

    for data in newDataset:
        if value in data[0][index]:
            subset = data
            break

    return findMostCommonLabel(subset)


def findTreeDepth(decisionTree):
    maxDepth = 0

    for branch in decisionTree:
        brokenBranch = branch.split()
        depth = int(brokenBranch[-2][0])

        if depth > maxDepth:
            maxDepth = depth

    return maxDepth


def calculatePrediction(testDataset, allFeatures, treeRootNode):
    if type(treeRootNode) == tree.Leaf:
        return treeRootNode.getValue()

    feature = treeRootNode.getFeatureName()
    builtTree = treeRootNode.getSubtree()
    index = allFeatures.index(feature)

    for i in range(len(builtTree)):
        if builtTree[i][0] == testDataset[index]:
            return calculatePrediction(testDataset, allFeatures, builtTree[i][1])


def getSubset(dataset, featureValue, index):
    for subset in dataset:
        if subset[0][index] == featureValue:
            return subset

    print("Im returning the whole dataset and not only a subset!")
    exit(1)


def getFeatureValues(dataset, index):
    values = []

    for dataPart in dataset:
        value = dataPart[index]

        if value not in values:
            values.append(value)

    return values


def sortTheHash(dictionary):
    newDict = {}
    array = sorted(dictionary.keys(), key=lambda x: x.lower())

    for key in array:
        newDict[key] = dictionary[key]

    return newDict


def findMostCommonLabel(dataset):
    goals = {}

    for dataPart in dataset:
        goal = dataPart[-1]
        if goal in goals.keys():
            goals[goal] += 1
        else:
            goals[goal] = 1

    goals = sortTheHash(goals)

    if len(goals.keys()) == 1:
        return [list(goals.keys())[0], True]

    return [max(goals, key=goals.get), False]


def getMostDiscriminatingFeature(dataset, features, allFeatures):
    informationGains = {}
    initialEntropy = getDatasetEntropy(dataset, len(dataset))

    for i in range(len(features)):
        if i == len(features) - 1:
            break

        feature = features[i]

        newDataset = datasetSorter(dataset, allFeatures.index(feature))
        informationGain = getDatasetInformationGain(newDataset, initialEntropy, len(dataset))
        informationGains[feature] = informationGain

    print(informationGains)

    return max(informationGains, key=informationGains.get)


def getDatasetEntropy(dataset, total):
    goals = {}

    for dataPart in dataset:

        goal = dataPart[-1]
        if goal in goals.keys():
            goals[goal] += 1
        else:
            goals[goal] = 1

    entropy = 0

    if len(goals.keys()) <= 1:
        return entropy

    for goal in goals.keys():
        entropy = entropy - goals[goal]/total * math.log2(goals[goal]/total)

    return entropy


def datasetSorter(dataset, index):
    newDataset = dataset.copy()

    sortedDataset = []
    usedValues = []

    for dataPart in newDataset:
        value = dataPart[index]
        if value in usedValues:
            sortedDataset[usedValues.index(value)].append(dataPart)
        else:
            usedValues.append(value)
            sortedDataset.append([dataPart])

    return sortedDataset


def getDatasetInformationGain(dataset, entropy, total):
    informationGain = entropy

    for dataSubset in dataset:
        informationGain = informationGain - len(dataSubset)/total * getDatasetEntropy(dataSubset, len(dataSubset))

    return informationGain