import math
import DecisionTree as tree


class ID3Model:
    def __init__(self, treeDepth):
        """
            Initializes the tree.
        @param treeDepth:
        """
        self.treeDepth = treeDepth
        if treeDepth != "":
            self.treeDepth = int(self.treeDepth)
        self.allFeatures = None
        self.decisionTree = None
        self.decisionTreeString = []
        self.stringCopy = []
        self.trainingDataset = None

    def findNewChildren(self, featureName, root, currentDepth, allowedDepth):
        """
            Trims the tree from specific node if depth is exceeded.
        @param featureName: Feature name.
        @param root: root node.
        @param currentDepth: depth of current node.
        @param allowedDepth: allowed depth.
        @return: trimmed node.
        """
        if type(root) is tree.Leaf:
            return [[featureName, root]]
        elif currentDepth >= allowedDepth:
            newRoot = self.findDemocracyValue(root)
            return [[featureName, newRoot]]
        else:
            return [[featureName, root]]

    def fit(self, trainingDataset):
        """
            Creates the tree and fits is features.
        @param trainingDataset: training dataset.
        """
        self.allFeatures = trainingDataset.pop(0)
        self.trainingDataset = trainingDataset
        self.decisionTree = self.id3Train(trainingDataset, trainingDataset, self.allFeatures.copy(), trainingDataset[0][-1])
        self.getDecisionTreeString()
        self.stringCopy = self.decisionTreeString.copy()
        # self.printTree()
        self.adjustDepth(trainingDataset)
        self.decisionTreeString = []
        self.getDecisionTreeString()
        self.printTree()

    def findValues(self, node, values):
        """
            finds values of nodes subtree.
        @param node: node whose subtree is considered.
        @param values: counter of values.
        @return: expanded values dictionary.
        """
        children = node.getSubtree()

        for child in children:
            obj = child[1]
            if type(obj) is tree.Leaf:
                value = obj.getValue()
                if value in values.keys():
                    values[value] += 1
                else:
                    values[value] = 1
            elif type(obj) is tree.Node:
                values = self.findValues(obj, values)

        return values

    def findListValues(self, features):
        """
            configures indexes of features compared to training dataset.
        @param features: features list.
        @return: dictionary of values count.
        """
        indexes = []
        values = {}
        for _ in features:
            indexes.append(-1)

        for dataset in self.trainingDataset:
            if -1 not in indexes:
                break
            for feature in features:
                if feature in dataset:
                    indexes[features.index(feature)] = dataset.index(feature)

        for dataset in self.trainingDataset:
            appendFlag = True
            for i in range(len(indexes)):
                if dataset[indexes[i]] != features[i]:
                    appendFlag = False
                    break
            if appendFlag:
                if dataset[-1] in values.keys():
                    values[dataset[-1]] += 1
                else:
                    values[dataset[-1]] = 1

        return values

    def findAllValues(self, feature):
        """
            Counts values of a feature.
        @param feature: specific feature.
        @return: values of that feature
        """
        values = {}
        if type(feature) is list:
            values = self.findListValues(feature)

        else:
            for data in self.trainingDataset:
                if feature in data:
                    if data[-1] in values.keys():
                        values[data[-1]] += 1
                    else:
                        values[data[-1]] = 1

        return values

    def getFeatures(self, root, target, features):
        """
            Fetches all possible features.
        @param root: root node.
        @param target: target node.
        @param features: current known features.
        @return: updated features.
        """
        if type(root) is tree.Leaf:
            return

        if root == target:
            return features

        for child in root.getSubtree():
            features.append(child[0])

            newFeatures = self.getFeatures(child[1], target, features)
            if newFeatures:
                return newFeatures
            else:
                features.pop()

    def getHardValues(self, features):
        """
            Handles more difficult features and returns their values.
        @param features: features
        @return: number of specific values of a feature.
        """
        indexes = []
        featureValues = []

        for feature in features:
            x = feature.split("=")
            label = x[0]
            featureValue = x[1]

            indexes.append(self.allFeatures.index(label))
            featureValues.append(featureValue)

        values = {}

        for dataset in self.trainingDataset:
            appendFlag = True
            for i in range(len(indexes)):
                if dataset[indexes[i]] != featureValues[i]:
                    appendFlag = False
                    break
            if appendFlag:
                if dataset[-1] in values.keys():
                    values[dataset[-1]] += 1
                else:
                    values[dataset[-1]] = 1

        return values

    def expandTree(self, node, root, features):
        """
            Expands the tree.
        @param node: Node to be added.
        @param root: Root node.
        @param features: Features.
        @return: new Features.
        """
        if type(root) is tree.Leaf:
            return -1

        features.append(root.getValue())

        children = root.getSubtree()

        for child in children:
            appendFlag = False
            if type(child[1]) is tree.Node:
                features.append(child[0])
                appendFlag = True
            if child[1] == node:
                return features

            newFeatures = self.expandTree(node, child[1], features)
            if newFeatures != -1:
                return newFeatures

            if appendFlag:
                features.pop()
            features.pop()
            features.append(root.getValue())
        features.pop()
        return -1

    def locateNodeInTree(self, node):
        """
            This function locates a node within tree.
        @param node: Node to locate.
        @return: feature based location.
        """
        root = self.decisionTree
        features = [root.getValue()]
        children = root.getSubtree()

        for child in children:
            features.append(child[0])
            if child[1] == node:
                return features

            newFeatures = self.expandTree(node, child[1], features)
            if newFeatures != -1:
                return newFeatures
            features.pop()

    def newFindHardValues(self, node):
        """
            Basically another one because first one didn't work as expected.
        @param node: Node.
        @return: Values of node.
        """
        features = self.locateNodeInTree(node)

        newFeatures = [features[0]]
        features.pop(0)
        for i in range(len(features)):
            if i % 2 == 0:
                newFeatures[-1] += "=" + features[i]
            else:
                newFeatures.append(features[i])
        values = self.getHardValues(newFeatures)
        return values

    def findHardValues(self, node, value):
        """
            A third one.
        @param node: /
        @param value: /
        @return: /
        """
        substring = node.getValue() + "=" + value
        features = ""

        for part in self.stringCopy:
            if substring in part:
                self.stringCopy.remove(part)
                features = part
                break

        features = features.split()[:self.treeDepth]

        newFeatures = []
        for feature in features:
            newFeatures.append(feature[2:])

        goalValues = self.getHardValues(newFeatures)

        return goalValues

    def nodeToLeaf(self, node, feature):
        """
            This function transforms a node into a leaf.
        @param node: Node to be transformed.
        @param feature: Its feature.
        @return: Leaf.
        """
        if not feature or feature == "True" or feature == "False" or feature == "Unknown":
            values = self.newFindHardValues(node)
        else:
            features = self.getFeatures(self.decisionTree, node, [])
            if features:
                values = self.findAllValues(features)
            else:
                values = self.findAllValues(feature)
        return getALeaf(values)

    def setChildren(self, oldChildren, newChildren):
        """
            Changes subtree.
        @param oldChildren: old tree children.
        @param newChildren: new tree children.
        @return: /
        """
        root = self.decisionTree

        if root.getSubtree() == oldChildren:
            root.setSubtree(newChildren)

        children = root.getSubtree()

        counter = 0

        while True:
            if counter == 100:
                break
            counter += 1
            nextChildren = []
            for child in children:
                node = child[1]
                if type(node) is tree.Leaf:
                    continue

                if node.getSubtree() == oldChildren:
                    node.setSubtree(newChildren)
                    return
                else:
                    for newChild in node.getSubtree():
                        nextChildren.append(newChild)
            children = nextChildren

    def cutTree(self, trainingDataset):
        """
            Cuts the tree to a depth.
        @param trainingDataset: training dataset.
        @return: trimmed tree.
        """
        if self.treeDepth == "":
            return

        if self.treeDepth == 0:
            self.decisionTree = tree.Leaf(findMostCommonLabel(trainingDataset))
            return

        if self.treeDepth == 1:
            children = self.decisionTree.getSubtree()
            newChildren = []
            for child in children:
                if type(child[1]) is tree.Leaf:
                    newChildren.append(child)
                    continue
                newChildren.append([child[0], self.nodeToLeaf(child[1], child[0])])

            self.decisionTree.setSubtree(newChildren)
            return

        currentTreeDepth = findTreeDepth(self.decisionTreeString)

        if currentTreeDepth < self.treeDepth:
            return
        else:
            root = self.decisionTree
            children = [root.getSubtree()]
            depth = 0

            while depth <= self.treeDepth - 1:
                newChildren = []
                for dataset in children:
                    currentChildren = []
                    oldChildren = []

                    for child in dataset:
                        node = child[1]
                        if depth == self.treeDepth - 1:
                            if type(node) is tree.Node:
                                leaf = self.nodeToLeaf(node, child[0])
                                currentChildren.append([child[0], leaf])
                                oldChildren.append(child)
                            else:
                                currentChildren.append(child)
                                oldChildren.append(child)
                        else:
                            if type(node) is tree.Node:
                                newChildren.append(node.getSubtree())
                    if depth == self.treeDepth - 1:
                        self.setChildren(oldChildren, currentChildren)
                children = newChildren
                depth += 1

    def getOptions(self, feature, dataset):
        """
            Find all options for a specific feature.
        @param feature: feature.
        @param dataset: dataset.
        @return: all possible feature values.
        """
        options = []
        index = self.allFeatures.index(feature)

        for data in dataset:
            if data[index] not in options:
                options.append(data[index])

        return options

    def adjustDepth(self, trainingDataset):
        """
            Handles tree trimming.
        @param trainingDataset: training dataset.
        """
        self.cutTree(trainingDataset)

    def getDecisionTreeString(self):
        """
            Prints the tree in string format to standard output. Used for testing.
        """
        self.printLevel("", self.decisionTree, 0)
        self.trimTree()

    def printTree(self):
        """
            Prints the formal tree to standard output.
        """
        print("[BRANCHES]:")

        for element in self.decisionTreeString:
            print(element)

    def trimTree(self):
        """
            Handles tree trimming.
        """
        newTree = []
        for element in self.decisionTreeString:
            if element == "":
                continue

            newTree.append(element)

        self.decisionTreeString = newTree
        self.decisionTreeString.sort()

    def printLevel(self, rootString, subtree, level):
        """
            Prints all nodes at level depth.
        @param rootString: root node in string format.
        @param subtree: root subtree.
        @param level: current level.
        @return: /
        """
        if type(subtree) == tree.Leaf:
            self.decisionTreeString[-1] = self.decisionTreeString[-1] + rootString + subtree.getValue()
            return

        level += 1
        rootFeature = subtree.getFeatureName()
        nextSubtree = subtree.getSubtree()

        rootString = rootString + str(level) + ":" + rootFeature + "="

        for element in nextSubtree:
            featureName = element[0]
            otherNextSubtree = element[1]

            self.decisionTreeString.append("")

            self.printLevel(rootString + featureName + " ", otherNextSubtree, level)

    def predict(self, testDataset):
        """
            Predicts values of features in test dataset based on built tree.
        @param testDataset: test dataset.
        @return: predictions array.
        """
        self.allFeatures = testDataset.pop(0)
        predictions = []

        for dataPart in testDataset:
            prediction = calculatePrediction(dataPart[:-1], self.allFeatures, self.decisionTree)

            if not prediction:
                prediction = self.decisionTree.getSubtree()[-1][1].getValue()
            predictions.append(prediction)

        return predictions

    def id3Train(self, reducedTrainingDataset, parentTrainingDataset, features, classLabel):
        """
            This function builds the tree from scratch.
        @param reducedTrainingDataset: Current training subset.
        @param parentTrainingDataset: previous training subset.
        @param features: Features.
        @param classLabel: label of current iteration.
        @return: Nodes and Leafs that are inserted into the tree.
        """
        if len(reducedTrainingDataset) == 0:
            leaf = tree.Leaf(findMostCommonLabel(parentTrainingDataset))
            return leaf

        cleanLabel = findMostCommonLabel(reducedTrainingDataset)
        leaf = tree.Leaf(cleanLabel.pop(0))
        cleanLabel = cleanLabel[0]

        if len(features) == 1 or cleanLabel:
            return leaf

        mostDiscriminatingFeature = getMostDiscriminatingFeature(reducedTrainingDataset, features, self.allFeatures)
        subtrees = []

        index = self.allFeatures.index(mostDiscriminatingFeature)
        featureValues = getFeatureValues(reducedTrainingDataset, index)
        newFeatures = features.copy()
        newFeatures.remove(mostDiscriminatingFeature)

        for value in featureValues:
            newDataset = datasetSorter(reducedTrainingDataset, index)
            subset = getSubset(newDataset, value, index)

            t = self.id3Train(subset, reducedTrainingDataset, newFeatures, classLabel)
            subtrees.append([value, t])

        return tree.Node(mostDiscriminatingFeature, subtrees)

    def getAllLeafValues(self, subtree, values):
        """
            Finds leaf values only.
        @param subtree: subtree.
        @param values: values.
        @return: updated values.
        """
        if type(subtree) is tree.Leaf:
            value = subtree.getValue()
            if value in values.keys():
                values[value] += 1
            else:
                values[value] = 1
            return values

        newSubtree = subtree.getSubtree()

        for element in newSubtree:
            node = element[1]
            values = self.getAllLeafValues(node, values)

        return values

    def findDemocracyValue(self, subtree):
        """
            Reduces nodes subtree to a single value and changes node to leaf.
        @param subtree: subtree.
        @return: Leaf.
        """
        allValues = self.getAllLeafValues(subtree, {})
        allValues = sorted(allValues, key=lambda x: (x[1], x[0]))

        newRoot = tree.Leaf(allValues[0])
        return newRoot


def getAllValues(subtree, values):
    """
        Finds all values within subtree.
    @param subtree: subtree.
    @param values: current values.
    @return: new values.
    """
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
    """
        Finds most common label for a feature and changes feature value to it.
    @param trainingDataset: training dataset.
    @param value: value.
    @param parentFeature: parent feature.
    @param allFeatures: all features.
    @return: most common label.
    """
    index = allFeatures.index(parentFeature)

    newDataset = datasetSorter(trainingDataset, index)
    subset = []

    for data in newDataset:
        if value in data[0][index]:
            subset = data
            break

    return findMostCommonLabel(subset)


def findTreeDepth(decisionTree):
    """
        Finds depth of a full tree (untrimmed).
    @param decisionTree: tree.
    @return: depth.
    """
    maxDepth = 0

    for branch in decisionTree:
        brokenBranch = branch.split()
        depth = int(brokenBranch[-2][0])

        if depth > maxDepth:
            maxDepth = depth

    return maxDepth


def calculatePrediction(testDataset, allFeatures, treeRootNode):
    """
        Calculates predictions.
    @param testDataset: test dataset.
    @param allFeatures: all features.
    @param treeRootNode: tree root.
    @return: predictions array.
    """
    if type(treeRootNode) == tree.Leaf:
        return treeRootNode.getValue()

    feature = treeRootNode.getFeatureName()
    builtTree = treeRootNode.getSubtree()
    index = allFeatures.index(feature)

    for i in range(len(builtTree)):
        if builtTree[i][0] == testDataset[index]:
            return calculatePrediction(testDataset, allFeatures, builtTree[i][1])


def getSubset(dataset, featureValue, index):
    """
        finds subset of a specific feature.
    @param dataset: dataset.
    @param featureValue: value of feature of interest.
    @param index: feature index.
    @return: subset.
    """
    for subset in dataset:
        if subset[0][index] == featureValue:
            return subset

    print("Im returning the whole dataset and not only a subset!")
    exit(1)


def getFeatureValues(dataset, index):
    """
        Finds feature possible values.
    @param dataset: dataset.
    @param index: feature index.
    @return: possible values.
    """
    values = []

    for dataPart in dataset:
        value = dataPart[index]

        if value not in values:
            values.append(value)

    values.sort()

    return values


def sortTheHash(dictionary):
    """
        Sorts dictionary.
    @param dictionary: dictionary.
    @return: sorted dictionary.
    """
    newDict = {}
    array = sorted(dictionary.keys(), key=lambda x: x.lower())

    for key in array:
        newDict[key] = dictionary[key]

    return newDict


def findMostCommonLabel(dataset):
    """
        Finds most common label.
    @param dataset: /
    @return: /
    """
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
    """
        Finds most discriminating feature.
    @param dataset: dataset.
    @param features: features.
    @param allFeatures: all features.
    @return: most discriminating feature.
    """
    informationGains = {}
    initialEntropy = getDatasetEntropy(dataset, len(dataset))

    for i in range(len(features)):
        if i == len(features) - 1:
            break

        feature = features[i]
        newDataset = datasetSorter(dataset, allFeatures.index(feature))

        informationGain = getDatasetInformationGain(newDataset, initialEntropy, len(dataset))
        informationGains[feature] = informationGain

    informationGains = dict(sorted(informationGains.items(), key=lambda x: x[1], reverse=True))
    # print(informationGains)

    return max(informationGains, key=informationGains.get)


def getDatasetEntropy(dataset, total):
    """
        Finds dataset entropy.
    @param dataset: dataset.
    @param total: total number of feature values.
    @return: entropy.
    """
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
    """
        Sorts dataset.
    @param dataset: dataset.
    @param index: feature index.
    @return: sorted dataset.
    """
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
    """
        Calculates information gain.
    @param dataset: dataset.
    @param entropy: entropy.
    @param total: total feature values.
    @return: information gain.
    """
    informationGain = entropy

    for dataSubset in dataset:
        a = getDatasetEntropy(dataSubset, len(dataSubset))
        informationGain = informationGain - len(dataSubset)/total * a

    return informationGain


def reduceDataset(feature, dataset):
    """
        Reduces dataset to only one feature.
    @param feature: feature of interest.
    @param dataset: dataset.
    @return: reduced dataset.
    """
    newDataset = []

    for data in dataset:
        if feature in data:
            newDataset.append(data)

    return newDataset


def getALeaf(values):
    """
        Creates a leaf from values list.
    @param values: values.
    @return: leaf.
    """
    maxValue = 0
    maxKeys = []

    for key in values.keys():
        if values[key] > maxValue:
            maxKeys = [key]
            maxValue = values[key]
        elif values[key] == maxValue:
            maxKeys.append(key)

    maxKeys.sort()

    return tree.Leaf(maxKeys[0])


def getValuesFromDataset(dataset, index):
    """
        Finds values of a feature in dataset.
    @param dataset: dataset.
    @param index: feature index.
    @return: values.
    """
    values = {}

    for data in dataset:
        if data[index] not in values.keys():
            values[data[index]] = 1
        else:
            values[data[index]] += 1

    return values


def getLeaves(dataset, options, classLabel):
    """
        Creates possible options leaves.
    @param dataset: dataset.
    @param options: leaf options.
    @param classLabel: class label.
    @return: leaves array.
    """
    leaves = []
    for option in options:
        reducedSet = reduceDataset(option, dataset)
        index = -1
        for data in dataset:
            if classLabel in data:
                index = data.index(classLabel)
        leaf = getALeaf(getValuesFromDataset(reducedSet, index))
        leaves.append([option, leaf])

    return leaves
