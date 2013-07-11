# coding: utf-8

import os
import pickle

meta = {}

def extrai_table_name(meta_name):
    return meta_name.split('_')

def main():
    for meta_data in os.listdir("banco/meta-data"):
        meta_file = os.path.join("banco/meta-data", meta_data)
        meta_name = meta_data.replace(".txt", "")
        table_name = extrai_table_name(meta_name)[1]
        table_timestamp = extrai_table_name(meta_name)[0]
        text_file = open(meta_file, "r", encoding="utf-8")
        data = text_file.read()
        columns = data.split('\n')
        meta[table_name] = []
        for column in columns:
            if column:
                values = column.split('\t')
                nome = values[0]
                tipo = values[1]
                desc = values[2]
                meta[table_name].append((nome, tipo, desc.encode('utf-8')))

    print(meta)
    out_file = open('grafo.pickle', 'wb')
    out_file.write(pickle.dumps(meta))
    out_file.close()

main()
