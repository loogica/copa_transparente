# coding: utf-8

# import simples
import io

#import com mudança de namespace
import urllib.request as request

# Atrbuição
# String
# Constante
# Junção com \
MES_09_12_URL = 'http://www.portaldatransparencia.gov.br/copa2014/gestor/' \
                'download?nomeArquivo=201209_BaseDados.zip'

# Inteiro
# Constante
BUFF_SIZE = 1024

# Função
# Nome "main"
# Argumentos Nenhum
def main():
    # Identação

    # Chamada de função
    response = request.urlopen(MES_09_12_URL)

    # Conversão de string para inteiro
    length = int(response.getheader('Content-Length'))

    # Conversão de float para inteiro
    times = int((length / BUFF_SIZE) + 1)

    # Imprime variáveis locais
    print(locals())

    # I/O usando io.FileIO
    out_file = io.FileIO("saida.zip", mode="w")

    # Loop de 0 até "times"
    for time in range(times):
        # Escreve em "out_file" o que ler em "response"
        out_file.write(response.read(BUFF_SIZE))
        print("Downloaded %d" % (((time * BUFF_SIZE)/length)*100))

    # Fecha Response
    response.close()
    # Fecha io.FileIO
    out_file.close()
    print("Finished")

main()
