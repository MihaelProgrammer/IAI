class Node:
    def __init__(self, featureName, subtree):
        self.featureName = featureName
        self.subtree = subtree

    def __str__(self):
        return f"Name: {self.featureName} Children: {str(self.subtree)}"

    def getValue(self):
        return self.featureName

    def getFeatureName(self):
        return self.featureName

    def getSubtree(self):
        return self.subtree

    def addChild(self, newChild):
        self.subtree.append(newChild)

    def setSubtree(self, newSubtree):
        self.subtree = newSubtree
        return self

    def getCurrentNode(self):
        return self


class Leaf:
    def __init__(self, leafValue):
        self.value = leafValue

    def getValue(self):
        return self.value

    def setValue(self, newValue):
        self.value = newValue
        return self

    def getCurrentNode(self):
        return self
