from DataLoader import fileReader
from RefutationResolution import refutationResolutionCG

import re


def nicifyCommand(command):
    """
        This function creates a more robust clause from given command.

    @param command: user input command
    @return: clause
    """
    clause = []

    for element in command:
        if element == "v" or element == "V":
            continue

        clause.append(element)

    return clause


def nicifyData(base):
    """
        This function creates a more robust dataset of clauses.

    @param base: clause set
    @return: updated clause set
    """
    newBase = []

    for clause in base:
        newBase.append(re.split(r' v | V ', clause))

    return newBase


def removeClauseFromBase(base, clause):
    """
        This function removes the specified clause from the clause set.

    @param base: clause set
    @param clause: clause to remove
    @return: updated clause set
    """
    if " v " in clause[0] or " V " in clause[0]:
        clause = re.split(r' v | V ', clause[0])

    for currentClause in base:
        if set(currentClause) == set(clause):
            base.remove(currentClause)
            print("Successfully removed ", clause, ".", sep="")
            break

    return base


def addClauseToBase(base, clause):
    """
        This function adds the given clause to clause set.

    @param base: clause set
    @param clause: clause to add
    @return: updated clause set
    """
    if " v " in clause[0] or " V " in clause[0]:
        clause = re.split(r' v | V ', clause[0])

    if clause not in base:
        base.append(clause)
        print("Successfully added ", clause, ".", sep="")

    return base


def handleCommand(clauses, command):
    """
        This function handles adding and removing from clause set.

    @param clauses: clause set
    @param command: command to execute
    @return: new, updated clause set
    """
    newCommand = command.split()

    if "+" in newCommand:
        clauses = addClauseToBase(clauses, nicifyCommand([command[:-2]]))
    else:
        clauses = removeClauseFromBase(clauses, nicifyCommand([command[:-2]]))

    return clauses


def prepareData(clauses, goal):
    """
        This function prepares data to be executable in resolution part of program.

    @param clauses: clause set
    @param goal: goal clause
    """
    newClauses = [clauses, [], [goal]]

    refutationResolutionCG(newClauses, goal[0])


def assistant(clauses, inputs):
    """
        This function executes all user inputs.

    @param clauses: clause set
    @param inputs: user inputs
    """
    for command in inputs:
        print("User input: ", command)
        if "?" in command:
            newCommand = command.split()
            prepareData(clauses, nicifyCommand(newCommand[:-1]))
        elif "+" in command or "-" in command:
            clauses = handleCommand(clauses, command)
        else:
            print("Fatal error: Undefined input!")
            exit(1)

        print()


def cookingAssistant(clauseFilepath, inputFilepath):
    """
        This function runs the cooking assistant part of the task.

    @param clauseFilepath: path to the file containing clauses
    @param inputFilepath: "user" input
    """
    clauses = nicifyData(fileReader(clauseFilepath))
    inputs = fileReader(inputFilepath)
    assistant(clauses, inputs)
