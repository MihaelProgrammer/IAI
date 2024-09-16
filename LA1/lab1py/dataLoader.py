"""
This files purpose is loading and adjustment of all data for easier handling later.
"""


def dataLoader(descriptorPath, mode):
    """
        This is the main function of a file that loads all data and processes it further to adjust and nicify it.

    :param descriptorPath: Path to descriptor file.
    :param mode: File type.
    :return: Returns a dictionary; either state-space descriptor or heuristic descriptor.
    """
    descriptor = []

    # Load the descriptor
    f = open(descriptorPath, "r", encoding="utf8")
    for line in f.readlines():
        if line[0] == "#":
            continue

        descriptor.append(line.rstrip())
    f.close()

    descriptor = dataNicifier(descriptor, mode)

    return descriptor


def dataNicifier(descriptor, mode):
    """
        This function divides 2 descriptors so each one is handled by a separate function.
        
    :param descriptor: Descriptor data
    :param mode: mode
    :return: Returns a dictionary; either state-space descriptor or heuristic descriptor
    """
    data = {}

    if mode == "ss":
        data = nicifyStateSpace(descriptor)
    elif mode == "h":
        data = nicifyHeuristic(descriptor)

    return data


def nicifyStateSpace(stateSpaceDescriptor):
    """
        This function handles the state-space descriptors data.
        
    :param stateSpaceDescriptor: State-space descriptor data
    :return: Dictionary containing descriptors data
    """
    
    # First handle the starting and goal states
    stateSpaceData = {"startingState": stateSpaceDescriptor.pop(0),
                      "goalStates": stateSpaceDescriptor.pop(0).split()}

    # Handle rest of the descriptor
    for line in stateSpaceDescriptor:
        fractionedLine = line.split()

        # Initialize current state array in dictionary
        currentState = fractionedLine.pop(0)[:-1]
        stateSpaceData[currentState] = []

        # Append every possible nextState to the array
        for nextState in fractionedLine:
            stateSpaceData[currentState].append(nextState.split(","))

    return stateSpaceData


def nicifyHeuristic(heuristicDescriptor):
    """
        This function handles the heuristic descriptors data.

    :param heuristicDescriptor: Heuristic descriptors data
    :return: Dictionary containing descriptors data
    """
    heuristicData = {}

    # Fill up the dictionary
    for line in heuristicDescriptor:
        state, heuristicValue = line.split()

        state = state[:-1]

        heuristicData[state] = float(heuristicValue)

    return heuristicData
