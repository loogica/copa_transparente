# coding: utf-8

import csv
import decimal
import locale
import os
import pickle
import sys

from copa_transparente.query import select

#locale.setlocale(locale.LC_ALL, "pt_BR")

in_file = open("grafo1.pickle", "rb")
grafo = pickle.loads(in_file.read())
in_file.close()

def fix_line(line, max_rows):
    ret = []
    for i, data in enumerate(line):
        if i >= max_rows:
            break
        if data.endswith('"'):
            new_data = line.pop(i + 1)
            data = "".join([data, new_data])
        ret.append(data)
    return ret



def extrai_table_name(meta_name):
    return meta_name.split('_')

def process(table_name):
    files = os.listdir('banco/data')
    data_file_path = None
    for f in files:
        fixex_table_name = extrai_table_name(f)[1]
        if fixex_table_name.startswith(table_name):
            data_file_path = os.path.join('banco/data', f)

    if not data_file_path:
        print('Nome errado de tabela')

    data_file = os.path.basename(data_file_path)
    meta_name = data_file.replace(".csv", "")
    table_name = extrai_table_name(meta_name)[1]
    table_timestamp = extrai_table_name(meta_name)[0]
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

    if table_name == "ExecucaoFinanceira":
        query = select("IdExecucaoFinanceira", "ValContrato")._from(table)
        print("Total dos gastos: {}".format(sum(map(lambda x: x[1], query))))
    else:
        for data in select()._from(table):
            print(data)

def main():
    if len(sys.argv) > 1:
        process(sys.argv[1])
    else:
        print('Informe a tabela')
main()
