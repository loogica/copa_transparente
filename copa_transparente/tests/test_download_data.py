import unittest
from unittest import mock

from copa_transparente.commands import download_dados_copa


HEADER_URL = 'http://www.portaldatransparencia.gov.br/copa2014/gestor/' \
             'download?nomeArquivo=201209_BaseDados.zip'

NO_LENGTH_HEADER = 'http://www.portaldatransparencia.gov.br/copa2014/gestor/' \
                   'download?nomeArquivo=20130711_BaseDados.zip'


class DownloadTest(unittest.TestCase):
    @unittest.skip('Untestable code')
    def test_download_main(self):
        download_dados_copa.main()

    def test_download_with_known_length(self):
        response = mock.MagicMock()
        response.read = mock.MagicMock(side_effect=['Data']*2)

        output = mock.MagicMock()
        output.write = mock.MagicMock()

        download_dados_copa.download_length(response, output, 1025)

        calls = [mock.call(download_dados_copa.BUFF_SIZE),
                 mock.call(download_dados_copa.BUFF_SIZE)]

        response.read.assert_has_calls(calls)

        calls = [mock.call('Data'),
                 mock.call('Data')]

        output.write.assert_has_calls(calls)

    def test_download_with_no_length(self):
        response = mock.MagicMock()
        response.read = mock.MagicMock(side_effect=['data', 'more data', ''])

        output = mock.MagicMock()
        output.write = mock.MagicMock()

        download_dados_copa.download(response, output)

        calls = [mock.call(download_dados_copa.BUFF_SIZE),
                 mock.call(download_dados_copa.BUFF_SIZE),
                 mock.call(download_dados_copa.BUFF_SIZE)]

        response.read.assert_has_calls(calls)

        calls = [mock.call('data'),
                 mock.call('more data')]

        output.write.assert_has_calls(calls)
