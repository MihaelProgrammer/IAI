from DataLoader import fileReader

# All the repeated pairs that shouldn't be revisited
repeated = []
# All clauses with their corresponding counters used for deduction
output = {}


def pickSecond(clause1, clauseSet):
    """
        This function picks the second clause from the clause set that would be a best fit to chosen first one.

    @param clause1: earlier chosen clause
    @param clauseSet: clause set
    @return: second clause if a fit is found, else -1
    """
    global repeated

    for clause in clauseSet:
        for literal in clause:
            negated = negateLiteral(literal)
            if isinstance(clause1, list):
                if negated in clause1:
                    if [clause1, clause] in repeated:
                        continue

                    return clause
            elif negated == clause1:
                if [clause1, clause] in repeated:
                    continue
                return clause

    return -1


def setOfSupportStrategy(clauses, goals):
    """
        One of main strategies for choosing clause sets from which clauses will be picked.

    @param clauses: clause set to choose from
    @param goals: goals
    @return: possible clause pairs, else -1
    """
    possibilities = []

    for clause1 in goals:
        clause2 = pickSecond(clause1, clauses)

        if clause2 == -1:
            continue

        if isinstance(clause2, list):
            if isinstance(clause1, list):
                possibilities.append([clause1, clause2])
            else:
                possibilities.append([[clause1], clause2])
        else:
            if isinstance(clause1, list):
                possibilities.append([clause1, [clause2]])

            possibilities.append([[clause1], [clause2]])

    if possibilities:
        return possibilities

    return -1


def negateClause(clause):
    """
        This method negates a clause.

    @param clause: clause to negate
    @return: negated clause
    """
    newClause = []

    for literal in clause:
        newClause.append(negateLiteral(literal))

    return newClause


def negateLiteral(literal):
    """
        This method negates a single literal. Yes, I do need it, why do you ask?

    @param literal: literal to be negated
    @return: negated literal
    """
    if isinstance(literal, list):
        literal = literal[0]
    if "~" in literal:
        return literal[1:]

    return "~" + literal


def deletionStrategy(clauseSet, mode):
    """
        Another important strategic method that deletes unnecessary clauses from clause set.

    @param clauseSet: clause set, duh
    @param mode: No clue why I need this, but I think it has to do something with the looks of clause set.
        Don't ask future me, he won't know either.
    @return: updated clause set
    """
    # Initialization

    newClauses = []
    if mode == 0:
        if len(clauseSet) <= 1:
            return clauseSet
        newClauses = clauseSet

    else:
        for newSet in clauseSet:
            newClauses = newClauses + newSet
        if not isinstance(newClauses[-1], list):
            newClauses[-1] = [newClauses[-1]]

    # Redundant clauses removal

    irrelevant = []

    for i in range(len(newClauses)):
        for j in range(i + 1, len(newClauses)):
            if set(newClauses[i]).issubset(set(newClauses[j])):
                irrelevant.append(newClauses[j])
            if set(newClauses[j]).issubset(set(newClauses[i])):
                irrelevant.append(newClauses[i])

    # Irrelevant clauses removal

    if mode == 0:
        for clause in irrelevant:
            if clause in newClauses:
                newClauses.remove(clause)

        for clause in newClauses:
            for literal in clause:
                if negateLiteral(literal) in clause:
                    if clause in newClauses:
                        newClauses.remove(clause)

    else:
        for clause in irrelevant:
            for subset in clauseSet:
                if clause in subset:
                    subset.remove(clause)

        for subset in clauseSet:
            for clause in subset:
                if isinstance(clause, str):
                    break
                for literal in clause:
                    if negateLiteral(literal) in clause:
                        if clause in subset:
                            subset.remove(clause)

    # Final touch

    if mode == 0:
        return newClauses
    else:
        # clauseSet[-2] = newClauses
        return clauseSet


def factorize(clause):
    """
        LOL. #suchnecessity

    @param clause: clause to be factorized.
    @return: factorized clause
    """
    return list(set(clause))


def dataNicifier(clauses):
    """
        This method forms a more robust way to operate with clauses.

    @param clauses: clause set
    @return: updated, more robust clause set
    """
    newClauses = []

    for clause in clauses:
        newClause = []
        if " v " in clause and " V " in clause:
            pass
        elif " V " not in clause:
            newClause = clause.split(" v ")
        elif " v " not in clause:
            newClause = clause.split(" V ")

        newClauses.append(newClause)

    goal = newClauses.pop()

    goals = []

    if " v " not in goal and " V " not in goal:
        for element in goal:
            goals.append([negateLiteral(element)])

        if len(goals) == 1:
            return [newClauses, [], goals[0]]

        return [newClauses, [], goals]

    return [newClauses, [], negateClause(goal)]


def pickClauses(clauses, goals):
    """
        This method picks 2 optimal clauses from the clause set to resolve into a new one. Well, at least shes trying.
            Note to future self. The earlier comment WAS about looks of clauses (mode was needed because [[], [], []]).

    @param clauses: clause set
    @param goals: goal clauses
    @return: 2 clauses that should be resolved
    """
    newClauses = []

    if not clauses[1]:
        currentClauses = clauses[0]

        for clause in currentClauses:
            newClauses.append(factorize(clause))

        for goal in goals:
            if not isinstance(goal, list):
                newClauses.append([goal])
            else:
                newClauses.append(goal)

        newClauses = deletionStrategy(newClauses, 0)

        pickedClauses = setOfSupportStrategy(newClauses, goals)

        if pickedClauses == -1:
            pickedClauses = setOfSupportStrategy(clauses[-3], newClauses[-1])
            if pickedClauses == -1:
                solutions = []

                for goal in goals:
                    for clause in newClauses:
                        if isinstance(clause, list) and isinstance(goal, list):
                            solutions.append([goal, clause])
                        elif isinstance(clause, list) and isinstance(goal, str):
                            solutions.append([[goal], clause])
                        elif isinstance(clause, str) and isinstance(goal, list):
                            solutions.append([goal, [clause]])
                        else:
                            solutions.append([[goal], [clause]])

                if len(solutions) == 1:
                    if len(solutions[0]) != 2:
                        return []
                    else:
                        return solutions[0]

                return solutions

        return pickedClauses

    else:
        newClauses.append([])
        newClauses.append([])

        for clause in clauses[0]:
            newClauses[0].append(factorize(clause))

        for clause in clauses[1]:
            newClauses[1].append(factorize(clause))

        newClauses.append(goals)

        newClauses = deletionStrategy(newClauses, 1)

        sos = [goals] + newClauses[1]
        pickedClauses = setOfSupportStrategy(sos, sos)

        if pickedClauses == -1:
            pickedClauses = setOfSupportStrategy(newClauses[0], sos)
            if pickedClauses == -1:
                solutions = []

                for goal in [goals] + newClauses[1]:
                    for clause in newClauses[0]:
                        if isinstance(clause, list):
                            if [goal, clause] not in repeated:
                                solutions.append([goal, clause])
                        else:
                            if [goal, [clause]] not in repeated:
                                solutions.append([goal, [clause]])

                return findBestPair(solutions, [goals] + newClauses[1])

        return pickedClauses


def findBestPair(pairs, derived):
    """
        I thought we passed this one, but I obviously have 2. Of course I need them both, what kind of a
            question is that?

    @param pairs: all possibilities for resolving
    @param derived: already derived pairs? clauses? who will know at this point...
    @return: all possible good matches for resolving
    """
    possibilities = []

    for pair in pairs:
        if len(pair) != 2:
            return possibilities
        first = pair[0].copy()
        second = pair[1].copy()

        if len(first) == 1:
            first = negateLiteral(first)
        else:
            first = negateClause(first)

        if first not in second:
            continue

        if first == second:
            possibilities.append(pair)
            continue

        second.remove(first)

        derivedFlag = 0

        for element in derived:
            if set(element).issubset(set(second)):
                derivedFlag = 1
                break

        if derivedFlag:
            continue

        possibilities.append(pair)

    if possibilities:
        return possibilities


def resolve(clause1, clause2):
    """
        Kill them both.

    @param clause1: first suicidal clause
    @param clause2: second suicidal clause
    @return: their baby
    """
    newClause = []

    first = clause1.copy()
    second = clause2.copy()

    for literal1 in first:
        for literal2 in second:
            if literal1 == negateLiteral(literal2):
                first.remove(literal1)
                second.remove(literal2)

    for literal1 in first:
        newClause.append(literal1)
    for literal2 in second:
        newClause.append(literal2)

    if len(newClause) == 0:
        return "NIL"

    return newClause


def clauseSetToNormalForm(clauseSet):
    """
        I have no clue why I needed this, but if its there, I needed it at some point so I made it.
            I hope name is descriptive enough.

    @param clauseSet: *waves a magic wand* CLAUSE SET! _insert applause here_
    @return: clause set in normal form? I guess?
    """
    normalForm = []

    for subset in clauseSet:
        if isinstance(subset, list):
            for clause in subset:
                if isinstance(clause, list):
                    string = ""
                    for literal in clause:
                        string = string + literal + " v "
                    string = string[:-3]
                    normalForm.append(string)
                else:
                    normalForm.append(clause)
        else:
            normalForm.append(subset)

    return normalForm


def checkForSubset(clauses, checkingSet):
    """
        This function checks if one clause set is subset to the other clause set.
            Don't ask me what that means, learn your math.

    @param clauses: clause set
    @param checkingSet: set we're checking against. Or vice versa. Who cares, it's a boolean.
    @return: True or False boolean value
    """
    newClauses = clauseSetToNormalForm(clauses)
    newCheckingSet = clauseSetToNormalForm(checkingSet)

    if set(newCheckingSet).issubset(newClauses):
        return True

    return False


def printClauses(clauseSet, counter):
    """
        This function prints clauses. Many of them. As many as it gets.

    @param clauseSet: set of clauses that needs to be crucified to standard output
    @param counter: index of the clause in the dictionary
    @return: counter value after all the hard work (Get it, cuz printing is slow)
    """
    global output

    if len(clauseSet) == 1:
        if isinstance(clauseSet[0], list):
            counter += 1
            print(counter, ". ", clauseSet[0][0], sep="")
            output[counter] = clauseSet[0]

            return counter
        counter += 1
        print(counter, ". ", clauseSet[0], sep="")
        output[counter] = clauseSet

        return counter

    for clause in clauseSet:
        counter += 1
        print(counter, ". ", sep="", end="")
        if len(clause) == 1 and isinstance(clause, list):
            print(clause[0])
            output[counter] = [clause[0]]
        elif len(clause) == 2 and clause[0] == "~":
            output[counter] = [clause]
            print(clause)
        else:
            newClause = ""

            for i in range(len(clause)):
                if i + 1 == len(clause):
                    print(clause[i])
                    newClause = newClause + str(clause[i])
                else:
                    print(clause[i], " v ", sep="", end="")
                    newClause = newClause + str(clause[i]) + " v "

            output[counter] = newClause.split(" v ")

    return counter


def printClause(resolvents, counter):
    """
        Same as above, but without the "s". Prints one clause only, usually when resolvent is found.

    @param resolvents: resolvents of suicidal clauses
    @param counter: counter value
    @return: new counter value
    """
    if len(resolvents) == 1:
        counter += 1
        print(counter, ". ", resolvents[0], sep="", end="")

    else:
        counter += 1
        print(counter, ". ", sep="", end="")
        for i in range(len(resolvents)):
            if i + 1 == len(resolvents):
                print(resolvents[i], end="")
            else:
                print(resolvents[i], " v ", sep="", end="")

    output[counter] = resolvents

    return counter


def printUsage(first, second):
    """
        Just the letters in the brackets signifying which clauses were used in deduction.
            What can I say, I realized too late I had to implement that.

    @param first: first clause index
    @param second: value of cupcakes in little red riding hoods basket after the inflation.
    """
    values = list(output.values())
    keys = list(output.keys())

    for value in values:
        if set(value) == set(first):
            print(" (", keys[values.index(value)], ", ", sep="", end="")
            break

    for value in values:
        if set(value) == set(second):
            print(keys[values.index(value)], ")", sep="", end="")
            break

    print()


def refutationResolutionAlgorithm(clauses, goal):
    """
        Main algorithm. A lot of stuff going on. It does its job. Honest pay for honest work.

    @param clauses: clause set
    @param goal: https://www.youtube.com/watch?v=7flz6hbOB5I
    @return: wait, it returns something?
    """
    global repeated

    newClauses = []
    counter = 0
    print(clauses)

    for clauseSet in clauses:
        if not clauseSet:
            continue
        counter = printClauses(clauseSet, counter)

    print("===============")

    while True:
        goals = clauses[-1]
        picked = pickClauses(clauses, goals)

        if not picked:
            print("[CONCLUSION]: ", goal, " is unknown", sep="")
            return False

        for pair in picked:
            if len(pair) != 2:
                print("[CONCLUSION]: ", goal, " is unknown", sep="")
                return False

            resolvents = resolve(pair[0], pair[1])
            if "NIL" in resolvents:
                print(counter + 1, ". NIL", sep="", end="")
                printUsage(pair[0], pair[1])
                print("===============")
                print("[CONCLUSION]: ", goal, " is true", sep="")
                return True
            if resolvents not in newClauses:
                newClauses.append(resolvents)
                counter = printClause(resolvents, counter)
                printUsage(pair[0], pair[1])
            else:
                repeated.append(pair)

        if checkForSubset(clauses.copy(), newClauses.copy()):
            print("===============")
            print("[CONCLUSION]: ", goal, " is unknown", sep="")
            return False

        for clause in newClauses:
            if clause not in clauses[1]:
                clauses[1].append(clause)


def refutationResolutionCG(clauses, goals):
    """
        Same as below function, but this one is used from the cookbook part of the program.

    @param clauses: clause set
    @param goals: goals
    """
    global repeated
    repeated = []

    if " v " in goals or " V " in goals:
        newGoals = negateClause(goals)
    else:
        newGoals = negateLiteral(goals)

    if isinstance(newGoals, list):
        clauses[-1] = newGoals
    else:
        clauses[-1] = [newGoals]

    refutationResolutionAlgorithm(clauses, goals)


def refutationResolution(filePath):
    """
        This function runs the resolution part of the task.

    @param filePath: #pileFath
    """
    clauses = fileReader(filePath)
    goalClause = clauses[-1]
    clauses = dataNicifier(clauses)

    refutationResolutionAlgorithm(clauses, goalClause)
