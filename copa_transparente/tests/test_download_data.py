import os
import shutil
import unittest

from unittest import mock


from copa_transparente.commands import download_dados_copa


class DownloadTest(unittest.TestCase):
    def setUp(self):
        self._test_path = "banco_teste"
        self.addCleanup(self._loca_file_cleanup, (self._test_path))

    @unittest.skip('Untestable code')
    def test_download_main(self):
        download_dados_copa.main()

    def test_download_url(self):
        name1 = 'copa_transparente.commands.download_dados_copa.download'
        name2 = 'copa_transparente.commands.download_dados_copa.download_length'
        name3 = 'copa_transparente.commands.download_dados_copa.request'
        name4 = 'copa_transparente.commands.download_dados_copa.io'

        getheader_mock = mock.MagicMock()
        getheader_mock.getheader = mock.MagicMock(side_effect=[1024])
        urlopen_mock = mock.MagicMock(side_effect=[getheader_mock])
        file_io_mock = mock.MagicMock()

        with mock.patch(name3) as request_mock:
            with mock.patch(name4) as io_mock:
                with mock.patch(name2) as down_len_mock:
                    with mock.patch(name1) as down_mock:
                        request_mock.urlopen = urlopen_mock
                        io_mock.FileIO.return_value = file_io_mock
                        download_dados_copa.download_url("url", "file_path")
                        urlopen_mock.assert_called_with("url")
                        getheader_mock.close.assert_called_with()
                        file_io_mock.close.assert_called_with()
                        #down_mock.assert_called_with(getheader_mock,
                        #                             file_io_mock)
                        down_len_mock.assert_called_with(getheader_mock,
                                                         file_io_mock, 1024)

        getheader_mock = mock.MagicMock()
        getheader_mock.getheader = mock.MagicMock(side_effect=[None])
        urlopen_mock = mock.MagicMock(side_effect=[getheader_mock])
        file_io_mock = mock.MagicMock()

        with mock.patch(name3) as request_mock:
            with mock.patch(name4) as io_mock:
                with mock.patch(name2) as down_len_mock:
                    with mock.patch(name1) as down_mock:
                        request_mock.urlopen = urlopen_mock
                        io_mock.FileIO.return_value = file_io_mock
                        download_dados_copa.download_url("url", "file_path")
                        urlopen_mock.assert_called_with("url")
                        getheader_mock.close.assert_called_with()
                        file_io_mock.close.assert_called_with()
                        down_mock.assert_called_with(getheader_mock,
                                                     file_io_mock)



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

    def test_extract_zip(self):
        zip_path = os.path.join(os.path.dirname(__file__),
                                "resources", "test.zip")

        test_path = "banco_teste"
        download_dados_copa.extract_zip(zip_path, path=test_path)

        data_path = os.path.join(test_path, "data")
        meta_data_path = os.path.join(test_path, "meta-data")
        self.assertTrue(os.path.exists(data_path))
        self.assertTrue(os.path.exists(meta_data_path))
        self.assertTrue(len(os.listdir(meta_data_path)) > 0)
        self.assertTrue(len(os.listdir(data_path)) > 0)

    def _loca_file_cleanup(self, path):
        if os.path.exists(path):
            shutil.rmtree(path)
