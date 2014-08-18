import datetime
import sys


from copa_transparente.commands import download_dados_copa


SITE = 'http://www.portaldatransparencia.gov.br'
SITE_PATH = '/copa2014/gestor/download?nomeArquivo={}_BaseDados.zip'


def main():
    if len(sys.argv) > 1:
        timestamp = sys.argv[1]
    else:
        timestamp = datetime.datetime.now().strftime("%Y%m%d")

    url = SITE + SITE_PATH.format(timestamp)
    download_dados_copa.download_url(url, "data_{}.zip".format(timestamp))
    download_dados_copa.extract_zip("data_{}.zip".format(timestamp))
    download_dados_copa.read_meta_data()


if __name__ == "__main__":
    main()
