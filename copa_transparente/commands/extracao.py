# coding: utf-8

import csv
import decimal
import io
import locale
import os
import pickle
import sys


from copa_transparente.query import select
from copa_transparente.utils import fix_line, extract_table_name


def table_detail(table_name):
    relations = {}
    in_file = open("banco/datamodel.pickle", "rb")
    grafo = pickle.loads(in_file.read())
    in_file.close()

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


def table_list():
    relations = {}
    in_file = open("banco/datamodel.pickle", "rb")
    grafo = pickle.loads(in_file.read())
    in_file.close()

    for name, table in grafo.items():
        print(name)


def show_data(table_name):
    in_file = open("banco/datamodel.pickle", "rb")
    grafo = pickle.loads(in_file.read())
    in_file.close()

    files = os.listdir('banco/data')
    data_file_path = None
    for f in files:
        _, fixex_table_name = extract_table_name(f)
        if fixex_table_name.startswith(table_name):
            data_file_path = os.path.join('banco/data', f)

    if not data_file_path:
        print('Nome errado de tabela')

    data_file = os.path.basename(data_file_path)
    meta_name = data_file.replace(".csv", "")
    table_timestamp, table_name = extract_table_name(meta_name)
    text_file = open(data_file_path, "r", encoding="utf-8")
    reader = csv.reader(text_file, delimiter=';', quotechar='"', skipinitialspace=True)

    print("Dados de {0}".format(table_name))
    table = grafo[table_name]

    line_count = 0
    for line in reader:
        if len(line) == 1:
            continue
        line = fix_line(line, len(table._columns))
        try:
            table.add_data(line)
            line_count += 1
        except Exception:
            print("Erro na linha {}".format(line_count))

    for data in select()._from(table):
        print(data)

