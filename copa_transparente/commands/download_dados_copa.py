# coding: utf-8

import datetime
import io
import sys
import logging

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
    except Exception as e:
        raise Exception("Erro no download do arquivo {}".format(url))
    finally:
        response.close()
        out_file.close()

def main():
    url = sys.argv[1]
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    download_url(url, "data_{}.zip".format(timestamp))

if __name__ == "__main__":
    main()
