import pickle

def main():
    relations = {}
    in_file = open("grafo1.pickle", "rb")
    grafo = pickle.loads(in_file.read())
    in_file.close()

    for name, table in grafo.items():
        print(name)

main()
