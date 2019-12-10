from src.model.Grammar import readFromFile, menuGrammar


class Main:
    def main(self):
        print("1. Grammar")
        print("2. Parser")
        val = int(input("Choose option: "))
        if val == 1:
            g = readFromFile("C:\\Users\\Darian\\Desktop\\LFTC\\ParsingLFTC\\src\\data\\grammar.txt")
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
                elif newVal == "5":
                    if g.isRegular():
                        print("The grammar is REGULAR")
                    else:
                        print("The grammar is NOT REGULAR")
                else:
                    break

main = Main()
main.main()
