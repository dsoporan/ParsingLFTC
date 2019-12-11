def menuParser():
    print("Choose option:")
    print("1. FIRST")
    print("2. FOLLOW")

class Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.firstSet = {}
        self.followSet = {}
        self.initializeFirstSet()
        self.initializeFollowSet()

    def initializeFirstSet(self):
        for left, right in self.grammar.P:
            self.firstSet[left] = [[]]

    def initializeFollowSet(self):
        for left, right in self.grammar.P:
            self.followSet[left] = []

    def computeFirstSet(self):
        index = 0
        for left, right in self.grammar.P:
            splittedRight = right[0].split(" ")
            self.firstSet[left][index].append(splittedRight[0])

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

    def computeFollowSet(self):
        self.followSet[self.grammar.S].append("E")

        for nonTerminal in self.grammar.N:
            # print("Non Terminal " + nonTerminal)
            for left, right in self.grammar.P:
                splittedRight = right[0].split(' ')
                # print("Right of productions" + str(splittedRight))
                if nonTerminal in splittedRight:
                    position = splittedRight.index(nonTerminal)
                    # print("Position" + str(position) + "Left" + str(left))
                    if len(splittedRight) >= position + 2:
                        position += 1
                        if not self.grammar.isTerminal(splittedRight[position]):
                            # print("First set of" + str(splittedRight[position]) + " " + str(self.firstSet[splittedRight[position]][-1]))
                            if 'E' in self.firstSet[splittedRight[position]][-1]:
                                # print("Ultim" + str(self.followSet[left]))
                                # print(splittedRight[position - 1])
                                self.followSet[splittedRight[position - 1]] = self.followSet[left].copy()
                                self.followSet[splittedRight[position - 1]].append(self.firstSet[splittedRight[position]][-1])
                            else:
                                self.followSet[splittedRight[position - 1]].append(self.firstSet[splittedRight[position]][-1])
                        else:
                            self.followSet[nonTerminal].append(splittedRight[position])
                    else:
                        self.followSet[splittedRight[position]] = self.followSet[left]

        for nonTerminal in self.grammar.N:
            lis = []
            for elem in self.followSet[nonTerminal]:
                if not isinstance(elem, list):
                    lis.append(elem)
                else:
                    for e in elem:
                        lis.append(e)
                lis = list(dict.fromkeys(lis))
                lis = list(dict.fromkeys(lis))
                self.followSet[nonTerminal] = lis
        print(self.followSet)
