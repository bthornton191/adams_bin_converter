import os
from pathlib import Path
import unittest
import subprocess

from itertools import product

from adams_bin_converter import convert

from test import TEST_FILE_DIR_MULTIPLE, TEST_FILE_DIR_SINGLE, TEST_FILE_DIR_VERSION_2021, TEST_GOOD_CMD_3
from test import CONVERTER_CMD, MULTI_MODEL_NAMES, TEST_GOOD_CMD_2
from test import clear_test_file_dir


class Test_ConvertApi(unittest.TestCase):

    def setUp(self):
        clear_test_file_dir()

    def test_convert_api_single_1(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks
        that all the cmd files are accounted for.
        """
        # Get the bin files
        bin_files = [f for f in TEST_FILE_DIR_SINGLE.glob('*.bin')]

        # Convert the bin files to cmd files
        for bin_file in bin_files:
            convert(bin_file)

        # Get a list of the newly created cmd files
        cmd_files = [f for f in TEST_FILE_DIR_SINGLE.glob('*.cmd') if f.name != 'aview.cmd']

        # Assert that there is a cmd file for every bin file
        self.assertListEqual([f.stem for f in bin_files], [f.stem for f in cmd_files])

    def test_convert_api_multiple_1(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks
        that all the cmd files are accounted for.
        """
        # Get the bin files
        bin_files = [f for f in TEST_FILE_DIR_MULTIPLE.glob('*.bin')]

        # Convert the bin files to cmd files
        for bin_file in bin_files:
            convert(bin_file)

        # Get a list of the newly created cmd files
        cmd_files = [f for f in TEST_FILE_DIR_MULTIPLE.glob('*.cmd') if f.name != 'aview.cmd']

        # Assert that there is a cmd file for every model in every bin file
        expected_cmd_files = [f'{mod}' for f, mod in product(bin_files, MULTI_MODEL_NAMES)]
        actual_cmd_files = [f.stem for f in cmd_files]

        self.assertListEqual(expected_cmd_files, actual_cmd_files)

    def tearDown(self):
        clear_test_file_dir()


class Test_ConvertCli(unittest.TestCase):

    def setUp(self):
        clear_test_file_dir()

    def test_convert_cli_use_bin_version(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks
        that all the cmd files are accounted for.
        """
        # Get the bin files
        bin_files = [f for f in TEST_FILE_DIR_SINGLE.glob('*.bin')]

        # Convert the bin files to cmd files
        cmd = 'python {} {}'.format(CONVERTER_CMD.absolute(), ' '.join([f.name for f in bin_files]))
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(
            cmd,
            cwd=TEST_FILE_DIR_SINGLE,
            startupinfo=startupinfo
        )

        process.wait()

        # Get a list of the newly created cmd files
        cmd_files = [f for f in TEST_FILE_DIR_SINGLE.glob('*.cmd') if f.name != 'aview.cmd']

        # Assert that there is a cmd file for every bin file
        self.assertListEqual([f.stem for f in bin_files], [f.stem for f in cmd_files])

    def test_convert_cli_specify_version_2019_1(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks
        that all the cmd files are accounted for.
        """
        # Get the bin files
        bin_files = [f for f in TEST_FILE_DIR_SINGLE.glob('*.bin')]

        # Convert the bin files to cmd files
        cmd = ' '.join([
            'python',
            '"{}"'.format(CONVERTER_CMD.absolute()),
            '--p',
            '"{}"'.format(TEST_GOOD_CMD_2),
            ' '.join([f.name for f in bin_files]),
        ])

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(
            cmd,
            cwd=TEST_FILE_DIR_SINGLE,
            startupinfo=startupinfo
        )

        process.wait()

        # Get a list of the newly created cmd files
        cmd_files = [f for f in TEST_FILE_DIR_SINGLE.glob('*.cmd') if f.name != 'aview.cmd']

        # Assert that there is a cmd file for every bin file
        self.assertListEqual([f.stem for f in bin_files], [f.stem for f in cmd_files])

    def test_convert_cli_specify_too_old_version(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks
        that all the cmd files are accounted for.
        """
        # Get the bin files
        bin_files = [f for f in TEST_FILE_DIR_VERSION_2021.glob('*.bin')]

        # Convert the bin files to cmd files
        cmd = ' '.join([
            'python',
            '"{}"'.format(CONVERTER_CMD.absolute()),
            '--p',
            '"{}"'.format(TEST_GOOD_CMD_3),
            ' '.join([f.name for f in bin_files]),
        ])

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(
            cmd,
            cwd=TEST_FILE_DIR_VERSION_2021,
            startupinfo=startupinfo
        )

        process.wait()

        # Get a list of the newly created cmd files
        cmd_files = [f for f in TEST_FILE_DIR_VERSION_2021.glob('*.cmd') if f.name != 'aview.cmd']

        # Assert that there is a cmd file for every bin file
        self.assertListEqual([], [f.stem for f in cmd_files])

    def tearDown(self):
        clear_test_file_dir()
