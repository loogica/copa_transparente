import io
import os
import pickle
import pprint
import sys

pp = pprint.PrettyPrinter(indent=4)

def main():
    relations = {}
    in_file = open("grafo1.pickle", "rb")
    grafo = pickle.loads(in_file.read())
    in_file.close()

    table_name = sys.argv[1]
    table = grafo[table_name]

    pks = {}
    for _table_name, meta in grafo.items():
        pk = meta.pk
        pks[pk.name] = meta

    print("PK  {:<30} Tipo {:<20}".format(table.pk.name, table.pk.kind))

    for column in table.cols[2:]:
        if column.name in pks:
            print("FK  {:<30} Tipo {:<20}".format(column.name, column.kind))
        else:
            print("Col {:<30} Tipo {:<20}".format(column.name, column.kind))

    print("{0} -> Outras".format(table_name))
    for relationship in table.references:
        print("   {}".format(relationship))
    print("Outras -> {0}".format(table_name))
    for relationship in table.referenced:
        print("   {}".format(relationship))

if __name__ == "__main__":
    main()
