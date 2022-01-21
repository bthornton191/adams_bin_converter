import os
from pathlib import Path
import unittest
import subprocess

from adams_bin_converter import convert

from test import TEST_FILE_DIR, CONVERTER_CMD, clear_test_file_dir

class Test_ConvertApi(unittest.TestCase):

    def setUp(self):
        clear_test_file_dir()

    def test_convert_api_1(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks 
        that all the cmd files are accounted for.
        """
        # Get the bin files
        bin_files = [f for f in TEST_FILE_DIR.glob('*.bin')]
        
        # Convert the bin files to cmd files
        for bin_file in bin_files:
            convert(bin_file)

        # Get a list of the newly created cmd files
        cmd_files = [f for f in TEST_FILE_DIR.glob('*.cmd') if f.name != 'aview.cmd']

        # Assert that there is a cmd file for every bin file
        self.assertListEqual([f.stem for f in bin_files], [f.stem for f in cmd_files])

    def tearDown(self):
        clear_test_file_dir()

class Test_ConvertCli(unittest.TestCase):

    def setUp(self):
        clear_test_file_dir()

    def test_convert_cli_1(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks 
        that all the cmd files are accounted for.
        """
        # Get the bin files
        bin_files = [f for f in TEST_FILE_DIR.glob('*.bin')]
        
        # Convert the bin files to cmd files
        cmd = 'python {} {}'.format(CONVERTER_CMD.absolute(), ' '.join([f.name for f in bin_files]))
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(
            cmd,
            cwd = TEST_FILE_DIR,
            startupinfo = startupinfo
        )

        process.wait()

        # Get a list of the newly created cmd files
        cmd_files = [f for f in TEST_FILE_DIR.glob('*.cmd') if f.name != 'aview.cmd']

        # Assert that there is a cmd file for every bin file
        self.assertListEqual([f.stem for f in bin_files], [f.stem for f in cmd_files])

    def tearDown(self):
        clear_test_file_dir()
        