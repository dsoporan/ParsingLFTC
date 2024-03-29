from src.model.Grammar import readFromFile, menuGrammar
from src.model.Parser import Parser, menuParser


class Main:
    def main(self):
        g = readFromFile("data/grammar.txt")
        print("Choose option: ")
        print("1. Grammar")
        print("2. Parser")
        val = int(input("Option: "))
        if val == 1:
            while 2:
                menuGrammar()
                newVal = input()
                if newVal == "1":
                    print(", ".join(g.N))
                elif newVal == "2":
                    print(", ".join(g.E))
                elif newVal == "3":
                    for left, right in g.P:
                        print(left + " -> " + "|".join(right))
                elif newVal == "4":
                    nonTerm = input("Give Non-Terminal:\n")
                    for left,right in g.P:
                        if left == nonTerm:
                            print(left + " -> " + "|".join(right))
                else:
                    break
        elif val == 2:
            parser = Parser(g)
            menuParser()
            parsVal = int(input("Option:"))
            while(parsVal):
                if parsVal == 1:
                    parser.computeFirstSet()
                    print(parser.firstSet)
                elif parsVal == 2:
                    parser.computeFirstSet()
                    parser.computeFollowSet()
                    print(parser.followSet)
                elif parsVal == 3:
                    inputSeq = input("Give a sequence each character separated by space: ")
                    parser.productionString(inputSeq)
                menuParser()
                parsVal = int(input("Option:"))


main = Main()
main.main()
