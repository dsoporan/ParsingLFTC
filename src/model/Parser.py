import numpy as np
import pandas as pd


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


        for nt in self.grammar.N:
            print(nt + " -> " )
            print( self.followSet[nt] )
            print( "\n")
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
                print(e)
                return e



    def makeTable(self):
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
                            A[l,c]=left + " -> " + e
                else:
                    lastel=firstl[len(firstl)-1]
                    for i in range(0,len(lastel)-1):
                        if lastel[i]==cols[c]:
                            left,e=self.getProdContStr(firstl[0][i],lines[l])
                            A[l,c]=left + "->" + e
                if "E" in firstl[len(firstl)-1]:
                    followl=self.followSet[lines[l]]
                    for e in followl:
                        if e==cols[c]:
                            val=self.getAPred(preds,lines[l])
                            A[l,c]=val



        print(df)

