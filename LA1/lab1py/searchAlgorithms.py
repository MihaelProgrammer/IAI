"""
This file creates a search tree from given descriptors for 3 different algorithms:
    1.) Breadth-first search
    2.) Uniform-cost search
    3.) A-star search
"""
import bisect

from treeStructure import NodeBFS
import heapq
# import time   #Used for timing evaluation in testing.


def printSolution(solutions):
    """
        This function is used for outputting solutions of each algorithm.

    :param solutions: Array containing solutions that should be output.
    """

    if solutions[0] == 0:
        print("[FOUND_SOLUTION]: no")

    else:
        print("[FOUND_SOLUTION]: yes")
        print("[STATES_VISITED]: ", solutions[1], sep="")
        print("[PATH_LENGTH]: ", solutions[2], sep="")
        print("[TOTAL_COST]: ", solutions[3], sep="")
        print("[PATH]: ", sep="", end="")

        for i in range(len(solutions[4])):
            if i == len(solutions[4]) - 1:
                print(solutions[4][i])
            else:
                print(solutions[4][i], " => ", sep="", end="")


def breadthFirstSearchHelper(stateSpaceDescriptor, startState, mode):
    """
            This function carries out Breadth-first search algorithm.

        :param stateSpaceDescriptor: State-space descriptor.
        :param startState: Starting state.
        :param mode: Checks if anything should be output.
        :return: Cost of the path, or prints specifications to standard output (depending on mode).
    """

    if mode:
        print("# BFS")

    # Initialize the tree
    startState = NodeBFS(startState, 0, 0, None)
    goalStates = stateSpaceDescriptor["goalStates"]

    # Build the tree
    openStates = [startState]
    statesVisited = set()

    while len(openStates) != 0:
        currentNode = openStates.pop(0)

        if currentNode.name in statesVisited:
            continue

        statesVisited.add(currentNode.name)

        if currentNode.name in goalStates:
            # Found the goal state
            solutions = [1, len(statesVisited), currentNode.depth + 1]
            totalCost = 0
            path = []

            while currentNode is not None:
                totalCost = totalCost + currentNode.distance
                path.append(currentNode.name)
                currentNode = currentNode.parent

            solutions.append(totalCost)
            path.reverse()
            solutions.append(path)
            if mode:
                printSolution(solutions)

            return totalCost

        nextStates = stateSpaceDescriptor[currentNode.name]
        nextStates.sort(key=lambda a: a[0])

        for states in nextStates:
            if states[0] in statesVisited:
                continue

            newNode = NodeBFS(states[0], currentNode.depth + 1, float(states[1]), currentNode)
            openStates.append(newNode)

    printSolution([0])
    return 0


def breadthFirstSearch(stateSpaceDescriptor, mode):
    """
        This function handles argument manipulation for BFS algorithm.
    @param stateSpaceDescriptor: State-space descriptor
    @param mode: mode for running the algorithm.
    @return: path cost, or outputs specifications.
    """
    return breadthFirstSearchHelper(stateSpaceDescriptor, stateSpaceDescriptor["startingState"], mode)


def uniformCostSearchHelper(stateSpaceDescriptor, startingState, mode):
    """
            This function carries out Uniform-cost search algorithm.

        :param stateSpaceDescriptor: State-space descriptor.
        :param startingState: Starting state.
        :param mode: Checks if anything should be output.
        :return: Outputs solutions to standard output.
        """

    if mode:
        print("# UCS")

    # timestamp = time.time()

    # Initialize the tree
    startState = NodeBFS(startingState, 0, 0, None)
    goalStates = stateSpaceDescriptor["goalStates"]

    # Build the tree
    statesVisited = set()
    openStates = [startState]
    heapq.heapify(openStates)

    while len(openStates) != 0:
        currentNode, openStates, statesVisited = fetchLowest(openStates, statesVisited)

        if currentNode.name in statesVisited:
            continue
        else:
            statesVisited.add(str(currentNode.name))

        if currentNode.name in goalStates:
            # Found the goal state
            solutions = [1, len(statesVisited), currentNode.depth + 1, currentNode.distance]
            path = []

            while currentNode is not None:
                path.append(currentNode.name)
                currentNode = currentNode.parent

            path.reverse()
            solutions.append(path)
            if mode:
                printSolution(solutions)

            return solutions[3]

        nextStates = stateSpaceDescriptor[currentNode.name]

        for states in nextStates:
            if states[0] in statesVisited:
                continue

            newNode = NodeBFS(states[0], currentNode.depth + 1, currentNode.distance + float(states[1]), currentNode)

            bisect.insort_left(openStates, newNode)

    printSolution([0])
    return 0


def fetchLowest(openStates, statesVisited):
    """
        This function finds the lowest cost node that hasn't been visited yet.
    @param openStates: array of open states.
    @param statesVisited: array of visited states.
    @return: next node to visit.
    """
    minNode = heapq.heappop(openStates)

    while minNode.name in statesVisited:
        minNode = heapq.heappop(openStates)

    return minNode, openStates, statesVisited


def uniformCostSearch(stateSpaceDescriptor, mode):
    """
        This function handles argument manipulation for UCS algorithm.
    @param stateSpaceDescriptor: State-space descriptor
    @param mode: mode for running the algorithm.
    @return: path cost, or outputs specifications.
    """
    return uniformCostSearchHelper(stateSpaceDescriptor, stateSpaceDescriptor["startingState"], mode)


def aStarSearchHelper(stateSpaceDescriptor, startingState, heuristicDescriptor, heuristicDescriptorPath, mode):
    """
            This function carries out A* search algorithm.

        :param stateSpaceDescriptor: State-space descriptor.
        :param startingState: Starting state.
        :param heuristicDescriptor: Heuristic descriptor.
        :param heuristicDescriptorPath: Name of heuristic descriptor file
        :param mode: Checks if anything should be output.
        :return: Outputs solutions to standard output.
        """

    if mode:
        heuristicName = heuristicDescriptorPath.split("/")[-1]
        print("# A-STAR ", heuristicName, sep="")

    # Initialize the tree
    startState = NodeBFS(startingState, 0, 0, None)
    goalStates = stateSpaceDescriptor["goalStates"]

    # Build the tree
    openStates = [startState]
    opened = [startState.name]
    statesVisited = set()
    closed = []
    closedStates = []
    iteration = 0

    while len(openStates) != 0:
        currentNode = openStates.pop(0)
        opened.pop(0)
        if currentNode.name not in statesVisited:
            statesVisited.add(currentNode.name)
        if currentNode.name in goalStates:
            # Found the goal state
            solutions = [1, len(statesVisited), currentNode.depth + 1]
            path = []
            solutions.append(currentNode.distance)

            while currentNode is not None:
                path.append(currentNode.name)
                currentNode = currentNode.parent

            path.reverse()
            solutions.append(path)
            if mode:
                printSolution(solutions)

            return solutions[3]
        closed.append(currentNode.name)
        closedStates.append(currentNode)
        nextStates = stateSpaceDescriptor[currentNode.name]
        # Sort them by heuristic value

        continuation = 0

        for states in nextStates:
            newNode = NodeBFS(states[0], currentNode.depth + 1, currentNode.distance + float(states[1]), currentNode)

            if newNode.name in closed or newNode.name in opened:
                if newNode.name in closed:
                    for node in closedStates:
                        if node.name == newNode.name:
                            if newNode.distance < node.distance:
                                closedStates.remove(node)
                                closed.remove(node.name)
                                break
                            else:
                                continuation = 1
                                break
                if newNode.name in opened:
                    for node in openStates:
                        if node.name == newNode.name:
                            if newNode.distance < node.distance:
                                openStates.remove(node)
                                opened.remove(node.name)
                                break
                            else:
                                continuation = 1

            if continuation:
                continuation = 0
                continue

            openStates.append(newNode)
            opened.append(newNode.name)

        openStates.sort(key=lambda a: (heuristicDescriptor[a.name] + a.distance, a.name))
        iteration += 1

    printSolution([0])
    return 0


def aStarSearch(stateSpaceDescriptor, heuristicDescriptor, heuristicDescriptorPath, mode):
    """
        This function handles argument manipulation for A* algorithm.
    @param stateSpaceDescriptor: State-space descriptor.
    @param heuristicDescriptor: heuristic for this algorithm.
    @param heuristicDescriptorPath: path to heuristic.
    @param mode: mode for running the algorithm.
    @return: path cost, or outputs specifications.
    """
    return aStarSearchHelper(stateSpaceDescriptor, stateSpaceDescriptor["startingState"], heuristicDescriptor, heuristicDescriptorPath, mode)
