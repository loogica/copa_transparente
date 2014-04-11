# coding: utf-8

import os
import pickle

from copa_transparente import domain


def extrai_table_name(meta_name):
    return meta_name.split('_')

def main():
    meta = {}
    for meta_data in os.listdir("banco/meta-data"):
        meta_file = os.path.join("banco/meta-data", meta_data)
        meta_name = meta_data.replace(".txt", "")
        table_name = extrai_table_name(meta_name)[1]
        table_timestamp = extrai_table_name(meta_name)[0]
        text_file = open(meta_file, "r", encoding="utf-8")
        data = text_file.read()
        columns = data.split('\n')
        meta[table_name] = domain.DataTable(table_name)
        ler_linhas(meta, table_name, columns)

    pks = {}

    for table_name, data_table in meta.items():
        pk = data_table.pk
        columns = data_table.cols[2:]
        pks[pk.name] = data_table
        for rel_table, rel_meta in meta.items():
            if rel_table != table_name:
                rel_pk = rel_meta.pk
                rel_columns = rel_meta.cols[2:]
                for column in rel_columns:
                    if column == pk:
                        data_table.add_referenced(column.name, rel_meta, column)

    for table_name, data_table in meta.items():
        columns = data_table.cols
        for column in columns:
            if column.name in pks:
                data_table.add_references(column.name, pks[column.name], column)


    out_file = open('grafo1.pickle', 'wb')
    out_file.write(pickle.dumps(meta))
    out_file.close()

def ler_linhas(meta, table_name, columns):
    for i, column in enumerate(columns):
        if column:
            values = column.split('\t')
            nome = values[0]
            tipo = values[1]
            desc = values[2]
            try:
                if i == 0:
                    meta[table_name].add_pk(nome, tipo, desc)
                else:
                    meta[table_name].add_column(nome, tipo, desc)
            except:
                print("Erro com Tabela {} Coluna {} tipo {}".format(table_name,
                                                                    nome,
                                                                    tipo))

if __name__ == "__main__":
    main()
