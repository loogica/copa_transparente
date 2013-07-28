# coding: utf-8

# import simples
import io
import sys

#import com mudança de namespace
import urllib.request as request

# Atrbuição
# String
# Constante
# Junção com \
HEADER_URL = 'http://www.portaldatransparencia.gov.br/copa2014/gestor/' \
             'download?nomeArquivo=201209_BaseDados.zip'

NO_LENGTH_HEADER = 'http://www.portaldatransparencia.gov.br/copa2014/gestor/' \
                   'download?nomeArquivo=20130711_BaseDados.zip'

#http://www.portaldatransparencia.gov.br/copa2014/gestor/download?nomeArquivo=201209_BaseDados.zip
#http://www.portaldatransparencia.gov.br/copa2014/gestor/download?nomeArquivo=20130711_BaseDados.zip


# Inteiro
# Constante
BUFF_SIZE = 1024

# Função
# Nome "main"
# Argumentos Nenhum
def main():
    # Identação

    # Chamada de função
    response = request.urlopen(sys.argv[1])

    # I/O usando io.FileIO
    out_file = io.FileIO("saida.zip", mode="w")

    content_length = response.getheader('Content-Length')
    if content_length:
        # Conversão de string para inteiro
        length = int(content_length)
        # Conversão de float para inteiro
        times = int((length / BUFF_SIZE) + 1)
        # Loop de 0 até "times"
        for time in range(times):
            # Escreve em "out_file" o que ler em "response"
            out_file.write(response.read(BUFF_SIZE))
            print("Downloaded %d" % (((time * BUFF_SIZE)/length)*100))
    else:
        total_downloaded = 0
        while True:
            # Escreve em "out_file" o que ler em "response"
            data = response.read(BUFF_SIZE)
            total_downloaded += len(data)
            if not data:
                break
            out_file.write(data)
            print('Downloaded {bytes}'.format(bytes=total_downloaded))

    # Fecha Response
    response.close()
    # Fecha io.FileIO
    out_file.close()
    print("Finished")

main()
