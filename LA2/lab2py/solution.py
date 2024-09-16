from RefutationResolution import refutationResolution
from CookingAssistant import cookingAssistant
import sys


def main():
    """
        Main program function. Heart of my work. Runs everything. Im proud of this one.
    """
    arguments = sys.argv[1:]

    if arguments[0] == "resolution":
        refutationResolution(arguments[1])
    elif arguments[0] == "cooking":
        cookingAssistant(arguments[1], arguments[2])
    else:
        print("Fatal error occured! Wrong keyword used!")
        exit(1)


if __name__ == "__main__":
    main()
