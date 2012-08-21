import configparser
import os
import unittest
from mock import Mock, MagicMock

from proton.template import Templates
from sitebaker import pages

file_spec = ['_CHUNK_SIZE', '__enter__', '__eq__', '__exit__',
             '__format__', '__ge__', '__gt__', '__hash__', '__iter__', '__le__',
             '__lt__', '__ne__', '__next__', '__repr__', '__str__',
             '_checkClosed', '_checkReadable', '_checkSeekable',
             '_checkWritable', 'buffer', 'close', 'closed', 'detach',
             'encoding', 'errors', 'fileno', 'flush', 'isatty',
             'line_buffering', 'mode', 'name',
             'newlines', 'peek', 'raw', 'read', 'read1', 'readable',
             'readinto', 'readline', 'readlines', 'seek', 'seekable', 'tell',
             'truncate', 'writable', 'write', 'writelines']

class HeadTest(unittest.TestCase):

    def setUp(self):
        templates = Templates('tests')
        templates['basic_test.html']

        mock_open = Mock(return_value = MagicMock(spec=file_spec))
        mock_open.return_value.read.return_value = 'this is a test'
        __builtins__['open'] = mock_open

        mock_stat = Mock(return_value = MagicMock(st_mtime = 100))
        self.orig_os_stat = os.stat
        os.stat = mock_stat

    def tearDown(self):
        if self.orig_os_stat:
            os.stat = self.orig_os_stat

    def test_head_generation(self):
        mock_config = MagicMock(spec=configparser.ConfigParser)

        page = pages.Page('test.text', '/tmp', 'testsite/test.html', mock_config)

        self.assertEqual('this is a test', page.full_content)
