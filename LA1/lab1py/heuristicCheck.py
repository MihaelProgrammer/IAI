"""
    This file serves a purpose of checking consistency and optimism of heuristic.
"""

from searchAlgorithms import breadthFirstSearchHelper, uniformCostSearchHelper, aStarSearchHelper


def heuristicConsistency(heuristicDescriptor, stateSpaceDescriptor):
    """
        This function checks for consistency of given heuristic.

    @param heuristicDescriptor: Heuristic descriptor
    @param stateSpaceDescriptor: State-space descriptor
    """
    keys = heuristicDescriptor.keys()
    wrongFlag = 0

    sorted(keys)

    for key in keys:
        value = heuristicDescriptor[key]
        neighbours = stateSpaceDescriptor[key]
        sorted(neighbours)
        for neighbour in neighbours:
            print("[CONDITION]: ", sep="", end="")
            if value <= heuristicDescriptor[neighbour[0]] + float(neighbour[1]):
                print("[OK] ", sep="", end="")
            else:
                print("[ERR] ", sep="", end="")
                wrongFlag = 1
            print("h(", key, ") <= h(", neighbour[0], ") + c: ", float(value), " <= ",
                  heuristicDescriptor[neighbour[0]], " + ", float(neighbour[1]), sep="")

    if wrongFlag:
        print("[CONCLUSION]: Heuristic is not consistent.")
    else:
        print("[CONCLUSION]: Heuristic is consistent.")


def heuristicOptimistic(heuristicDescriptor, stateSpaceDescriptor):
    """
        This function checks for optimism of a given heuristic.

    @param heuristicDescriptor: Heuristic descriptor
    @param stateSpaceDescriptor: State-space descriptor
    """
    keys = list(heuristicDescriptor.keys())
    keys.sort()
    wrongFlag = 0

    for key in keys:
        value = heuristicDescriptor[key]
        bfsCost = breadthFirstSearchHelper(stateSpaceDescriptor, key, 0)
        astarCost = aStarSearchHelper(stateSpaceDescriptor, key, heuristicDescriptor, "", 0)
        uniCost = uniformCostSearchHelper(stateSpaceDescriptor, key, 0)
        cost = min(bfsCost, astarCost, uniCost)

        print("[CONDITION]: ", sep="", end="")
        if value <= cost:
            print("[OK] ", sep="", end="")
        else:
            print("[ERR] ", sep="", end="")
            wrongFlag = 1
        print("h(", key, ") <= h*: ", float(value), " <= ", float(cost), sep="")

    if wrongFlag:
        print("[CONCLUSION]: Heuristic is not optimistic.")
    else:
        print("[CONCLUSION]: Heuristic is optimistic.")


def heuristicCheck(heuristicDescriptor, stateSpaceDescriptor, name, mode):
    """
        This function is main function of this file which prints main things
            to standard output and calls the right function based on what needs doing.

    @param heuristicDescriptor: Heuristic descriptor
    @param stateSpaceDescriptor: State-space descriptor
    @param name: Heuristic name
    @param mode: Consistency vs. optimism check
    """
    name = name.split("/")[-1]
    if mode == "opt":
        print("# HEURISTIC-OPTIMISTIC ", name, sep="")
        heuristicOptimistic(heuristicDescriptor, stateSpaceDescriptor)
    if mode == "con":
        print("# HEURISTIC-CONSISTENT ", name, sep="")
        heuristicConsistency(heuristicDescriptor, stateSpaceDescriptor)
