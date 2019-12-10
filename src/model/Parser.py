def menuParser():
    print("Choose option:")
    print("1. FIRST")
    print("2. FOLLOW")

class Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.firstSet = {}
        self.followSet = {}

    def initializeFirstSet(self):
        for left, right in self.grammar.P:
            self.firstSet[left] = [[]]

    def computeFirstSet(self):
        self.initializeFirstSet()
        index = 0
        for left, right in self.grammar.P:
            splittedRight = right[0].split(" ")
            self.firstSet[left][index].append(splittedRight[0])

        print(self.firstSet)

        index += 1
        while True:
            done = 0
            for nonTerminal in self.firstSet:
                if self.grammar.isTerminal(self.firstSet[nonTerminal][index-1][0]) or self.firstSet[nonTerminal][index-1][0] == 'E':
                    self.firstSet[nonTerminal].append(self.firstSet[nonTerminal][index-1])
                else:
                    self.firstSet[nonTerminal].append(self.firstSet[self.firstSet[nonTerminal][index-1][0]][index-1])
                    done += 1
            if done == 0:
                break
            index += 1

        print(self.firstSet)
