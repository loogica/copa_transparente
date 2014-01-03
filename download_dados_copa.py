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
#http://www.portaldatransparencia.gov.br/copa2014/gestor/download?nomeArquivo=20130923_BaseDados.zip


BUFF_SIZE = 1024
def download_length(response, output, length):
    times = length / BUFF_SIZE
    if length % BUFF_SIZE > 0:
        times += 1
    for time in range(int(times)):
        output.write(response.read(BUFF_SIZE))
        print("Downloaded %d" % (((time * BUFF_SIZE)/length)*100))

def download(response, output):
    total_downloaded = 0
    while True:
        # Escreve em "out_file" o que ler em "response"
        data = response.read(BUFF_SIZE)
        total_downloaded += len(data)
        if not data:
            break
        output.write(data)
        print('Downloaded {bytes}'.format(bytes=total_downloaded))


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
        length = int(content_length)
        download_length(response, out_file, length)
    else:
        download(response, out_file)

    # Fecha Response
    response.close()
    # Fecha io.FileIO
    out_file.close()
    print("Finished")

if __name__ == "__main__":
    main()
