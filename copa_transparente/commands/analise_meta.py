import io
import os
import pickle
import pprint
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             '../..'))
import copa_transparente

dotviz = '''
digraph Relations {
    node [shape = rectangle];
    %s
    %s
}
'''

pp = pprint.PrettyPrinter(indent=4)

def main():
    pks = {}
    relations = {}
    reverse_relations = {}

    in_file = open("grafo1.pickle", "rb")
    grafo = pickle.loads(in_file.read())
    in_file.close()

    for table, meta in grafo.items():
        pk = meta.pk
        pks[pk.name] = meta

    for table, meta in grafo.items():
        columns = meta.cols[2:]
        relations[table] = []
        for column in columns:
            if column.name in pks:
                relations[table].append((pks[column.name].name, column.name))

    tables = ""
    for table, meta in grafo.items():
        inner_text = "{}\n\n".format(table)
        for column in meta.cols:
            inner_text += "{}\n".format(column.name)
        tables += '{} [label="{}"];\n'.format(table, inner_text)

    out_file = open("relations.pickle", "wb")
    all_relations = dict(pks=pks, relations=relations, reverse=reverse_relations)
    out_file.write(pickle.dumps(all_relations))
    out_file.close()

    stringio = io.StringIO()
    for name, relations in relations.items():
        for relation in relations:
            stringio.write('    %s -> %s [label = "%s"];\n' % (name, relation[0], relation[1]))

    print(dotviz % (tables, stringio.getvalue()))

if __name__ == "__main__":
    main()
