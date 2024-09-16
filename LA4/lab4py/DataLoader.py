"""
This files purpose is loading and adjustment of all data for easier handling later.
"""


def getData(filePath):
    """
        This is the main function of a file that gets all data from a given file, processes it and returns it.

    @param filePath: Path to a file that needs to be read.
    @return: Returns 2D list of nicified contents.
    """
    return dataCaster(dataNicifier(fileLoader(filePath)))


def fileLoader(filePath):
    """
        This is a function that loads all data and processes it further to adjust and nicify it.

    @param filePath: Path to a file that needs to be read.
    @return: Returns file contents without comments.
    """
    contents = []

    # Load the file
    f = open(filePath, "r", encoding="utf8")
    for line in f.readlines():
        contents.append(line.rstrip())

    f.close()

    return contents


def dataNicifier(fileContents):
    """
        This function nicifies all data into more suitable form for later handling.

    @param fileContents: Contents of a read file.
    @return: Returns 2D list of nicified contents.
    """
    niceContents = []

    for line in fileContents:
        niceContents.append(line.split(","))

    return niceContents


def dataCaster(fileContents):
    """
        This function casts all values from string to float.
    @param fileContents: Contents of a read file.
    @return: Returns 2D list of float values.
    """
    castedContents = []

    for line in fileContents:
        castedLine = []

        for value in line:
            if "." in value:
                castedLine.append(float(value))
            else:
                castedLine.append(value)

        castedContents.append(castedLine)

    return castedContents
