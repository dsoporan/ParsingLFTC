import numpy as np
import pandas as pd


def menuParser():
    print("Choose option:")
    print("1. FIRST")
    print("2. FOLLOW")
    print("3. Computing Parsing Tree")

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

        # print(self.firstSet)

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


        # for nt in self.grammar.N:
        #     print(nt + " -> " )
        #     print( self.followSet[nt] )
        #     print( "\n")
        # print(self.followSet)

    def getProdContStr(self,char,nonTerm):
        for left, right in self.grammar.P:
            if left == nonTerm:
                for el in right:
                    if char in el:
                        return left,el





    def getProds(self,nonT):
        listt=[]
        for left, right in self.grammar.P:
            if left==nonT:
                listt.append(right)
        return listt

    def prediction(self):
        list=[]
        pred={}
        for a in self.grammar.N:
            list.append(a)


        for a in list:
            prods=self.getProds(a)
            for b in prods:
                for x in b:
                    val= str(a) + "->" + str(x)
                    pred[val]=[]
                    c=x.split(" ")
                    if self.grammar.isTerminal(c[0]):
                        pred[val].append(c[0])

                    elif self.grammar.isNonTerminal(c[0]):
                        lista=self.firstSet.get(c[0])
                        pred[val]=pred[val] + lista[-1]
                    elif c[0] == "E":
                        pred[val].append("E")
        return pred


    def getAPred(self,pred,nonT):
        a=pred.keys()
        for e in a:
            if nonT in e and pred.get(e)==["E"]:
                return 'E'



    def makeTable(self):
        self.computeFirstSet()
        self.computeFollowSet()
        cols=self.grammar.E
        cols.append("E")
        lines=self.grammar.N
        lines= lines + cols
        preds=self.prediction()


        A = np.empty([len(lines),len(cols)],dtype="S20")
        A[:]=' '
        df = pd.DataFrame(A, index=lines, columns=cols)
        for c in range(0, len(cols)):
            for l in range(0,len(lines)):
                if lines[l]==cols[c]:
                    A[l,c]='pop'
        A[len(lines)-1,len(cols)-1]='acc'

        for c in range(0, len(cols)):
            for l in range(0,len(lines)-len(cols)):
                firstl=self.firstSet[lines[l]]
                if len(firstl[0])==1:
                    for elem in firstl[len(firstl)-1]:
                        if elem==cols[c]:
                            left,e=self.getProdContStr(firstl[0][0],lines[l])
                            A[l,c]=e
                else:
                    lastel=firstl[len(firstl)-1]
                    for i in range(0,len(lastel)-1):
                        if lastel[i]==cols[c]:
                            left,e=self.getProdContStr(firstl[0][i],lines[l])
                            A[l,c]=e
                if "E" in firstl[len(firstl)-1]:
                    followl=self.followSet[lines[l]]
                    for e in followl:
                        if e==cols[c]:
                            val=self.getAPred(preds,lines[l])
                            A[l,c]=val

        print(df)
        print(A[0][2])
        return A

    def getProdNumber(self, left, right):
        index = 1
        for l, r in self.grammar.P:
            if l == left and r == right:
                return index
            index += 1

    def getProdOfNonterminal(self, nonTerminal):
        lis = []
        for left, right in self.grammar.P:
            if left == nonTerminal:
                lis.append(right)
        return lis

    def getAllTerminalsToComputeTable(self, nonTerminal):
        allTerminals = []
        fromFirst = self.firstSet[nonTerminal][-1]
        if 'E' in fromFirst:
            for term in fromFirst:
                allTerminals.append(term)
            for term in self.followSet[nonTerminal]:
                allTerminals.append(term)
        else:
            for term in fromFirst:
                allTerminals.append(term)
        allTerminals = list(dict.fromkeys(allTerminals))
        allTerminals = list(dict.fromkeys(allTerminals))
        return allTerminals

    def chooseProdThatSuits(self, prodForNonterminal, terminal):
        for prod in prodForNonterminal:
            if self.grammar.isTerminal(prod[0][0]) and prod[0][0] == terminal:
                return prod
        return prodForNonterminal[-1]


    def productionString(self, inputSequence):
        self.computeFirstSet()
        self.computeFollowSet()
        inputStack = inputSequence.split(' ')
        workingStack = [self.grammar.S]
        outputStack = []

        numberingProd = {}
        for nonTerminal in self.grammar.N:
            allTerminals = self.getAllTerminalsToComputeTable(nonTerminal)
            prodForNonterminal = self.getProdOfNonterminal(nonTerminal)
            for terminal in allTerminals:
                if len(prodForNonterminal) == 1:
                    numberingProd[(nonTerminal, terminal)] = (prodForNonterminal[0], self.getProdNumber(nonTerminal, prodForNonterminal[0]))
                else:
                    production = self.chooseProdThatSuits(prodForNonterminal, terminal)
                    numberingProd[(nonTerminal, terminal)] = (production, self.getProdNumber(nonTerminal, production))

        print(numberingProd)

        while len(workingStack) > 0:
            elem = workingStack[0]
            if self.grammar.isNonTerminal(elem):
                del workingStack[0]
                production = 0
                number = 0
                try:
                    if len(inputStack) > 0:
                        production, number = numberingProd[(elem, inputStack[0])]
                    else:
                        production, number = numberingProd[(elem, 'E')]
                except:
                    print("!Invalid input sequence! " + str(elem) + ", " + str(inputStack))
                    break
                splittedProduction = production[0].split(' ')
                index = 0
                for prod in splittedProduction:
                    if prod != 'E':
                        workingStack.insert(index, prod)
                        index += 1
                outputStack.append(number)
            else:
                if elem == inputStack[0]:
                    del workingStack[0]
                    del inputStack[0]
                elif elem != 'E':
                    print("!Invalid input sequence!")
                    break
                else:
                    del workingStack[0]

        print(outputStack)





