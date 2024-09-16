"""
This files purpose is loading and adjustment of all data for easier handling later.
"""


def fileReader(filePath):
    """
        This is the main function of a file that loads all data and processes it further to adjust and nicify it.

    :param filePath: Path to a file that needs to be read.
    :return: Returns file contents without comments.
    """
    contents = []

    # Load the file
    f = open(filePath, "r", encoding="utf8")
    for line in f.readlines():
        if line[0] == "#":
            continue

        contents.append(line.rstrip())
    f.close()

    return contents
