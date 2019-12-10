def menuGrammar():
    print("Choose option:\n")
    print("1. Set of Non-Terminals")
    print("2. Set of Terminals")
    print("3. Set of Productions")
    print("4. Set of Productions of a given non-terminal symbol")
    print("5. Check if the grammar is regular")

def readFromFile(filename):
    allProductions = []
    count = 0
    with open(filename) as file:
        line = file.readline()
        while line:
            if count == 0:
                N = line[:-1].split(",")
            elif count == 1:
                E = line[:-1].split(",")
            elif count == 2:
                S = line[:-1]
            else:
                leftRight = line[:-1].split("->")
                left = leftRight[0]
                right = leftRight[1]
                allRights = right.split("|")
                allProductions.append((left, allRights))
            count += 1
            line = file.readline()
    P = allProductions
    return Grammar(N, E, S, P)

class Grammar:
    def __str__(self) -> str:
        return 'N = { ' + ', '.join(self.N) + ' }\n' \
               + 'E = { ' + ', '.join(self.E) + ' }\n' \
               + 'S = ' + str(self.S) + '\n' \
               + 'P = { ' + str(self.P) + ' }\n'

    def isNonTerminal(self, value):
        return value in self.N

    def isTerminal(self, value):
        return value in self.E

    def isRegular(self):
        # Has to be terminal + non-terminal
        # Only 2 elements
        # epsilon can be in RHS but the symbol id is not allowed to be in rhs
        notAllowedInRHS = []
        usedRHS = []

        for rule in self.P:
            left,rightAll = rule
            print(left, rightAll)
            for right in rightAll:
                print(right)
                if len(right) > 2:
                    return False
                elif len(right) == 1:
                    if right[0] != 'E' and not self.isTerminal(right[0]):
                        return False
                    elif right[0] == 'E':
                        notAllowedInRHS.append(left)
                else:
                    if not (self.isTerminal(right[0]) and self.isNonTerminal(right[1])):
                        return False
                    usedRHS.append(right[1])

        for elem in notAllowedInRHS:
            if elem in usedRHS:
                return False

        return True

    def __init__(self, N, E, S, P):
        # NonTerminals
        self.N = N
        # Terminals
        self.E = E
        # Starting Symbol
        self.S = S
        # Productions
        self.P = P
