# coding: utf-8

import os
import pickle
import sys

data = {}
in_file = open("relations.pickle", "rb")
all_relations = pickle.loads(in_file.read())
in_file.close()

in_file = open("grafo.pickle", "rb")
grafo = pickle.loads(in_file.read())
in_file.close()

def extrai_table_name(meta_name):
    return meta_name.split('_')

def process(table_name):
    files = os.listdir('banco/data')
    data_file_path = None
    for f in files:
        if table_name in f:
            data_file_path = os.path.join('banco/data', f)

    if not data_file_path:
        print('Nome errado de tabela')

    data_file = os.path.basename(data_file_path)
    meta_name = data_file.replace(".csv", "")
    table_name = extrai_table_name(meta_name)[1]
    table_timestamp = extrai_table_name(meta_name)[0]
    text_file = open(data_file_path, "r", encoding="utf-8")
    content = text_file.read()
    lines = content.split('\n')
    data[table_name] = []
    print("Dados de {0}".format(table_name))
    print(grafo[table_name])
    for line in lines:
        if len(line.split(';')) == 1:
            continue
        print("\nNova linha\n")
        for column in line.split(';'):
            print(column.encode('utf-8'))


def main():
    if len(sys.argv) > 1:
        process(sys.argv[1])
    else:
        print('Informe a tabela')
main()
