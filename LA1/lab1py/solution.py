"""
This file is main file for solution.
"""

import sys
import searchAlgorithms
import dataLoader
import heuristicCheck


def argumentHandler(arguments):
    """
        This function handles configuration of arguments passed through the command line.
    @param arguments: CLI arguments
    @return: [spaceStateDescriptor, heuristicDescriptor, algorithm, heuristicOptimistic, heuristicConsistent]
    """
    algorithm, spaceStateDescriptor, heuristicDescriptor, heuristicOptimistic, heuristicConsistent = "", "", "", "", ""

    for i in range(len(arguments)):
        if arguments[i] == "--alg":
            algorithm = arguments[i + 1]
            i = i + 1
        if arguments[i] == "--ss":
            spaceStateDescriptor = arguments[i + 1]
            i = i + 1
        if arguments[i] == "--h":
            heuristicDescriptor = arguments[i + 1]
            i = i + 1
        if arguments[i] == "--check-optimistic":
            heuristicOptimistic = True
        if arguments[i] == "--check-consistent":
            heuristicConsistent = True

    return [spaceStateDescriptor, heuristicDescriptor, algorithm, heuristicOptimistic, heuristicConsistent]


def main():
    """
        Main function.
    """

    spaceStateDescriptorPath, heuristicDescriptorPath, algorithm,\
        heuristicOptimistic, heuristicConsistent = argumentHandler(sys.argv)

    stateSpaceDescriptor, heuristicDescriptor = "", ""

    if spaceStateDescriptorPath != "":
        stateSpaceDescriptor = dataLoader.dataLoader(spaceStateDescriptorPath, "ss")
    if heuristicDescriptorPath != "":
        heuristicDescriptor = dataLoader.dataLoader(heuristicDescriptorPath, "h")
    if algorithm != "":
        if algorithm == "bfs":
            searchAlgorithms.breadthFirstSearch(stateSpaceDescriptor, 1)
        elif algorithm == "ucs":
            searchAlgorithms.uniformCostSearch(stateSpaceDescriptor, 1)
        elif algorithm == "astar":
            searchAlgorithms.aStarSearch(stateSpaceDescriptor, heuristicDescriptor, heuristicDescriptorPath, 1)
        else:
            print("Unsupported algorithm! Use BFS, UCS or A*.")
            exit(1)
    if heuristicOptimistic:
        heuristicCheck.heuristicCheck(heuristicDescriptor, stateSpaceDescriptor, heuristicDescriptorPath, "opt")
    if heuristicConsistent:
        heuristicCheck.heuristicCheck(heuristicDescriptor, stateSpaceDescriptor, heuristicDescriptorPath, "con")


if __name__ == "__main__":
    main()
