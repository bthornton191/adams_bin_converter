import unittest
import os

import adams_bin_converter

from test import TEST_GOOD_CMD_1, TEST_GOOD_CMD_2, TEST_GOOD_CMD_3, TEST_BAD_CMD, TEST_FILE_DIR, clear_test_file_dir

class Test_GoodmvGoodev(unittest.TestCase):

    def setUp(self):
        clear_test_file_dir()
        adams_bin_converter.ADAMS_LAUNCH_COMMAND = TEST_GOOD_CMD_2
        os.environ['ADAMS_LAUNCH_COMMAND'] = str(TEST_GOOD_CMD_3)

    def test_convert_with_argument(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks 
        that all the cmd files are accounted for.
        """
        cmd_files = with_argument(TEST_GOOD_CMD_1)

        # Assert that there is a cmd file for every bin file
        self.assertListEqual([f.stem for f in TEST_FILE_DIR.glob('*.bin')], [f.stem for f in cmd_files])
    
    def test_convert_without_argument(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks 
        that all the cmd files are accounted for.
        """
        cmd_files = without_argument()

        # Assert that there is a cmd file for every bin file
        self.assertListEqual([f.stem for f in TEST_FILE_DIR.glob('*.bin')], [f.stem for f in cmd_files])

    def tearDown(self):
        clear_test_file_dir()
    
class Test_GoodmvNoev(unittest.TestCase):

    def setUp(self):
        clear_test_file_dir()
        adams_bin_converter.ADAMS_LAUNCH_COMMAND = TEST_GOOD_CMD_2
        _ = os.environ.pop('ADAMS_LAUNCH_COMMAND', None)

    def test_convert_with_argument(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks 
        that all the cmd files are accounted for.
        """
        cmd_files = with_argument(TEST_GOOD_CMD_1)

        # Assert that there is a cmd file for every bin file
        self.assertListEqual([f.stem for f in TEST_FILE_DIR.glob('*.bin')], [f.stem for f in cmd_files])
    
    def test_convert_without_argument(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks 
        that all the cmd files are accounted for.
        """
        cmd_files = without_argument()

        # Assert that there is a cmd file for every bin file
        self.assertListEqual([f.stem for f in TEST_FILE_DIR.glob('*.bin')], [f.stem for f in cmd_files])

    def tearDown(self):
        clear_test_file_dir()
    
class Test_NomvGoodev(unittest.TestCase):

    def setUp(self):
        clear_test_file_dir()
        os.environ['ADAMS_LAUNCH_COMMAND'] = str(TEST_GOOD_CMD_3)

    def test_convert_with_argument(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks 
        that all the cmd files are accounted for.
        """
        cmd_files = with_argument(TEST_GOOD_CMD_1)

        # Assert that there is a cmd file for every bin file
        self.assertListEqual([f.stem for f in TEST_FILE_DIR.glob('*.bin')], [f.stem for f in cmd_files])
    
    def test_convert_without_argument(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks 
        that all the cmd files are accounted for.
        """
        cmd_files = without_argument()

        # Assert that there is a cmd file for every bin file
        self.assertListEqual([f.stem for f in TEST_FILE_DIR.glob('*.bin')], [f.stem for f in cmd_files])

    def tearDown(self):
        clear_test_file_dir()
    
class Test_NomvNoev(unittest.TestCase):

    def setUp(self):
        clear_test_file_dir()
        _ = os.environ.pop('ADAMS_LAUNCH_COMMAND', None)

    def test_convert_with_argument(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks 
        that all the cmd files are accounted for.
        """
        cmd_files = with_argument(TEST_GOOD_CMD_1)

        # Assert that there is a cmd file for every bin file
        self.assertListEqual([f.stem for f in TEST_FILE_DIR.glob('*.bin')], [f.stem for f in cmd_files])
    
    def test_convert_without_argument(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks 
        that all the cmd files are accounted for.
        """
        with self.assertRaises(EnvironmentError):
            cmd_files = without_argument()

    def tearDown(self):
        clear_test_file_dir()
    
class Test_GoodmvBadev(unittest.TestCase):

    def setUp(self):
        clear_test_file_dir()
        adams_bin_converter.ADAMS_LAUNCH_COMMAND = TEST_GOOD_CMD_2
        os.environ['ADAMS_LAUNCH_COMMAND'] = str(TEST_BAD_CMD)

    def test_convert_with_argument(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks 
        that all the cmd files are accounted for.
        """
        cmd_files = with_argument(TEST_GOOD_CMD_1)

        # Assert that there is a cmd file for every bin file
        self.assertListEqual([f.stem for f in TEST_FILE_DIR.glob('*.bin')], [f.stem for f in cmd_files])
    
    def test_convert_without_argument(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks 
        that all the cmd files are accounted for.
        """
        cmd_files = without_argument()

        # Assert that there is a cmd file for every bin file
        self.assertListEqual([f.stem for f in TEST_FILE_DIR.glob('*.bin')], [f.stem for f in cmd_files])

    def tearDown(self):
        clear_test_file_dir()
    
class Test_BadmvGoodev(unittest.TestCase):

    def setUp(self):
        clear_test_file_dir()
        adams_bin_converter.ADAMS_LAUNCH_COMMAND = TEST_BAD_CMD
        os.environ['ADAMS_LAUNCH_COMMAND'] = str(TEST_GOOD_CMD_3)

    def test_convert_with_argument(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks 
        that all the cmd files are accounted for.
        """
        cmd_files = with_argument(TEST_GOOD_CMD_1)

        # Assert that there is a cmd file for every bin file
        self.assertListEqual([f.stem for f in TEST_FILE_DIR.glob('*.bin')], [f.stem for f in cmd_files])
    
    def test_convert_without_argument(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks 
        that all the cmd files are accounted for.
        """
        cmd_files = without_argument()

        # Assert that there is a cmd file for every bin file
        self.assertListEqual([f.stem for f in TEST_FILE_DIR.glob('*.bin')], [f.stem for f in cmd_files])

    def tearDown(self):
        clear_test_file_dir()
    
class Test_BadmvBadev(unittest.TestCase):

    def setUp(self):
        clear_test_file_dir()
        adams_bin_converter.ADAMS_LAUNCH_COMMAND = TEST_BAD_CMD
        os.environ['ADAMS_LAUNCH_COMMAND'] = str(TEST_BAD_CMD)

    def test_convert_with_argument(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks 
        that all the cmd files are accounted for.
        """
        cmd_files = with_argument(TEST_GOOD_CMD_1)

        # Assert that there is a cmd file for every bin file
        self.assertListEqual([f.stem for f in TEST_FILE_DIR.glob('*.bin')], [f.stem for f in cmd_files])
    
    def test_convert_without_argument(self):
        """Converts all the bin files in the test file directory to cmd files. Then checks 
        that all the cmd files are accounted for.
        """
        with self.assertRaises(OSError):
            cmd_files = without_argument()

    def tearDown(self):
        clear_test_file_dir()

def with_argument(adams_launch_command):
    # Get the bin files
    bin_files = [f for f in TEST_FILE_DIR.glob('*.bin')]
    
    # Convert the bin files to cmd files
    for bin_file in bin_files:
        adams_bin_converter.convert(bin_file, adams_launch_command)

    # Return a list of the newly created cmd files
    return [f for f in TEST_FILE_DIR.glob('*.cmd') if f.name != 'aview.cmd']

def without_argument():
    # Get the bin files
    bin_files = [f for f in TEST_FILE_DIR.glob('*.bin')]
    
    # Convert the bin files to cmd files
    for bin_file in bin_files:
        adams_bin_converter.convert(bin_file)

    # Return a list of the newly created cmd files
    return [f for f in TEST_FILE_DIR.glob('*.cmd') if f.name != 'aview.cmd']