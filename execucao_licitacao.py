# coding: utf-8

import csv
import decimal
import datetime
import math
import os
import pickle
import sys
import tempfile
import json

import humanize

from copa_transparente.query import select

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

def process():
    table_name = "ExecucaoFinanceira"

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
    new_file = open("temp.csv", "wt")

    while True:
        data = text_file.read(4096)
        if not data:
            break
        data = data.replace("\r\n", "")
        new_file.write(data)

    new_file.flush()
    new_file.close()

    text_file = open("temp.csv", "r", encoding="utf-8")
    original_lines = 0
    for line in text_file.readlines():
        original_lines += 1

    new_file = open("temp.csv", "rt")
    reader = csv.reader(new_file, delimiter=';', quotechar='"', skipinitialspace=True)

    print("Dados de {0}".format(table_name))
    table = grafo[table_name]

    valid_lines = 0
    for line in reader:
        if len(line) == 1:
            continue
        line = fix_line(line, len(table._columns))
        try:
            table.add_data(line)
            valid_lines += 1
        except Exception:
            print("Erro na linha {}".format(valid_lines))

# 4397 - 3606 = 791
# 3634 - 3606 = 28
# 791 / 4397

    missing_lines = original_lines - valid_lines
    error = float(missing_lines/original_lines)
    error_str = "{:.2%}".format(error)
    print("Total: {}".format(original_lines))
    print("Parsed: {}".format(valid_lines))
    print("Error Rate: {:.2%}".format(error))

    line_count = 0
    query = select("IdExecucaoFinanceira", "IdLicitacao", "ValContrato", "IdInstituicaoContratado")._from(table)
    for data in query:
        #print(data)
        line_count += 1
        pass
    print("Total de registros analisados : {} ({} perdidos)".format(line_count, missing_lines))

    query = select("IdExecucaoFinanceira", "IdLicitacao", "ValContrato")._from(table)
    total_com_licitacao = sum(map(lambda x: x[2], filter(lambda x: x[1], query)))
    print("Execução Financeira com referência para Licitação: {}".format(
          total_com_licitacao))

    query = select("IdExecucaoFinanceira", "IdLicitacao", "ValContrato")._from(table)
    total_sem_licitacao = sum(map(lambda x: x[2], filter(lambda x: not x[1], query)))
    print("Execução Financeira sem referência para Licitação: {}".format(
          total_sem_licitacao))

    query = select("IdExecucaoFinanceira", "IdLicitacao", "ValContrato")._from(table)
    total = sum(map(lambda x: x[2], query))
    print("Total dos gastos: {}".format(total))

    date_str = datetime.datetime.now().strftime("%d/%m/%Y")

    data = {
        'd_total': str(total),
        'd_total_sem_ref_lic': str(total_sem_licitacao),
        'd_total_com_ref_lic': str(total_com_licitacao),
        'total': humanize.intword(total).replace("billion", "bilhões"),
        'total_sem_ref_lic': humanize.intword(total_sem_licitacao).replace("billion", "bilhões"),
        'total_com_ref_lic': humanize.intword(total_com_licitacao).replace("billion", "bilhões"),
        'percentual_dados_desconsiderados': error_str,
        'atualizado': date_str
    }
    out = open("data.json", "wt")
    out.write(json.dumps(data))
    out.close()

    out = open("hist/data_{}.json".format(datetime.datetime.now().strftime("%Y%m%d")), "wt")
    out.write(json.dumps(data))
    out.close()
    print(data)

if __name__ == "__main__":
    process()
