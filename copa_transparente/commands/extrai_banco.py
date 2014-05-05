# coding: utf-8

import datetime
import os
import zipfile


def extract_zip(file_name):
    banco_zip = zipfile.ZipFile(file_name)
    banco_zip.extractall(path="banco")
    banco_zip.close()
    print("{} descomprimido".format(file_name))

    for tabela in os.listdir('banco'):
        nome_banco = os.path.join("banco", tabela)
        banco_zip = zipfile.ZipFile(nome_banco)
        banco_zip.extractall(path="banco")
        banco_zip.close()
        os.remove(nome_banco)
        print("Processado %s" % (nome_banco))

    print("Criando Base de Dados")
    os.chdir("banco")

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


def main():
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    extract_zip("data_{}.zip".format(timestamp))


if __name__ == "__main__":
    main()
