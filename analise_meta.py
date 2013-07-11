import io
import os
import pickle
import pprint

dotviz = '''
digraph Relations {
    node [shape = rectangle];
%s}
'''

pp = pprint.PrettyPrinter(indent=4)

def main():
    pks = {}
    relations = {}
    reverse_relations = {}

    in_file = open("grafo.pickle", "rb")
    grafo = pickle.loads(in_file.read())
    in_file.close()

    for table, meta in grafo.items():
        pk = meta[0][0]
        columns = meta[1:]
        context = {'table': table, 'pk': pk}
        pks[pk] = table
        reverse_relations[table] = []
        for rel_table, rel_meta in grafo.items():
            if rel_table != table:
                rel_pk = rel_meta[0][0]
                rel_columns = rel_meta[1:]
                for column in rel_columns:
                    if column[0] == pk:
                        reverse_relations[table].append((rel_table, rel_pk))

    for table, meta in grafo.items():
        columns = meta[1:]
        relations[table] = []
        for column in columns:
            if column[0] in pks:
                relations[table].append((pks[column[0]], column[0]))

    out_file = open("relations.pickle", "wb")
    all_relations = dict(pks=pks, relations=relations, reverse=reverse_relations)
    out_file.write(pickle.dumps(all_relations))
    out_file.close()

    stringio = io.StringIO()
    for name, relations in relations.items():
        for relation in relations:
            stringio.write('    %s -> %s [label = "%s"];\n' % (name, relation[0], relation[1]))

    print(dotviz % stringio.getvalue())

main()
