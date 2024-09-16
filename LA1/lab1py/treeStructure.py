class NodeBFS:
    """
        Class used for better state manipulation.
    """
    def __init__(self, name, depth, distance, parentNode):
        """
            Initialization method.

        :param name: Node name.
        :param depth: Node depth.
        :param distance: Node distance to root node.
        """

        self.name = name
        self.depth = depth
        self.distance = distance
        self.parent = parentNode
        self.adjacent = set()

    def __lt__(self, other):
        if self.distance == other.distance:
            return self.name < other.name

        return self.distance < other.distance

    def __repr__(self):
        return self.name
