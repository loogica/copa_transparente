# coding: utf-8

import datetime
import io
import logging
import os
import pickle
import sys
import zipfile

import urllib.request as request


from copa_transparente import domain, utils


BUFF_SIZE = 1024


def download_length(response, output, length):
    times = length / BUFF_SIZE
    if length % BUFF_SIZE > 0:
        times += 1
    for time in range(int(times)):
        output.write(response.read(BUFF_SIZE))
        logging.info("Downloaded %d" % (((time * BUFF_SIZE)/length)*100))


def download(response, output):
    total_downloaded = 0
    while True:
        data = response.read(BUFF_SIZE)
        total_downloaded += len(data)
        if not data:
            break
        output.write(data)
        logging.info('Downloaded {bytes}'.format(bytes=total_downloaded))


def download_url(url, file_path):
    response = request.urlopen(url)
    out_file = io.FileIO(file_path, mode="w")
    content_length = response.getheader('Content-Length')

    try:
        if content_length:
            length = int(content_length)
            download_length(response, out_file, length)
        else:
            download(response, out_file)
    except Exception:
        raise Exception("Erro no download do arquivo {}".format(url))
    finally:
        response.close()
        out_file.close()


def extract_zip(file_name, path="banco"):
    banco_zip = zipfile.ZipFile(file_name)
    banco_zip.extractall(path=path)
    banco_zip.close()

    for tabela in os.listdir(path):
        nome_banco = os.path.join(path, tabela)
        banco_zip = zipfile.ZipFile(nome_banco)
        banco_zip.extractall(path=path)
        banco_zip.close()
        os.remove(nome_banco)

    current_path = os.getcwd()
    os.chdir(path)

    if not os.path.exists("data"):
        os.mkdir("data")
    if not os.path.exists("meta-data"):
        os.mkdir("meta-data")

    for arquivo in os.listdir("."):
        if arquivo.endswith(".txt"):
            os.rename(arquivo, os.path.join("meta-data", arquivo))
        elif arquivo.endswith(".csv"):
            os.rename(arquivo, os.path.join("data", arquivo))
        else:
            pass

    os.chdir(current_path)


def read_meta_data():
    meta = {}
    for meta_data in os.listdir("banco/meta-data"):
        meta_file = os.path.join("banco/meta-data", meta_data)
        meta_name = meta_data.replace(".txt", "")
        table_timestamp, table_name = utils.extract_table_name(meta_name)
        text_file = open(meta_file, "r", encoding="utf-8")
        data = text_file.read()
        columns = data.split('\n')
        meta[table_name] = domain.DataTable(table_name)
        read_lines(meta, table_name, columns)

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


    out_file = open('banco/datamodel.pickle', 'wb')
    out_file.write(pickle.dumps(meta))
    out_file.close()


def read_lines(meta, table_name, columns):
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
