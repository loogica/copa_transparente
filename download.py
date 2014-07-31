import datetime
import sys


from copa_transparente.commands import download_dados_copa


def main():
    url = sys.argv[1]
    timestamp = datetime.datetime.now().strftime("%Y%m%d")

    download_dados_copa.download_url(url, "data_{}.zip".format(timestamp))
    download_dados_copa.extract_zip("data_{}.zip".format(timestamp))
    download_dados_copa.read_meta_data()


if __name__ == "__main__":
    main()
