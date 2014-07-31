# coding: utf-8

import datetime
import io
import logging
import os
import sys
import zipfile

import urllib.request as request


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

def main():
    url = sys.argv[1]
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    download_url(url, "data_{}.zip".format(timestamp))
    extract_zip("data_{}.zip".format(timestamp))


if __name__ == "__main__":
    main()
