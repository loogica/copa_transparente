import io
import os
import pickle
import pprint
import sys

pp = pprint.PrettyPrinter(indent=4)

def main():
    relations = {}
    in_file = open("grafo.pickle", "rb")
    grafo = pickle.loads(in_file.read())
    in_file.close()

    in_file = open("relations.pickle", "rb")
    all_relations = pickle.loads(in_file.read())
    in_file.close()

    tabela = grafo[sys.argv[1]]
    relations = all_relations['relations'][sys.argv[1]]
    reverse_relations = all_relations['reverse'][sys.argv[1]]
    print("PK {:<30} Tipo {:<20}".format(tabela[0][0], tabela[0][1]))
    for column in tabela[1:]:
        found = 0
        for relation in relations:
            if relation[1] == column[0]:
                found = 1
                print("FK  {:<30} Tipo {:<20}".format(column[0], column[1]))
        if not found:
            print("Col {:<30} Tipo {:<20}".format(column[0], column[1]))

    pp.pprint(relations)
    pp.pprint(reverse_relations)

if __name__ == "__main__":
    main()

