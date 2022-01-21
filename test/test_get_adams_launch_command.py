import unittest
import os
from pathlib import Path
import adams_bin_converter

from test import TEST_BAD_CMD, TEST_GOOD_CMD_1, TEST_GOOD_CMD_2, TEST_GOOD_CMD_3

class Test_GoodmvGoodev(unittest.TestCase):

    def setUp(self):
        adams_bin_converter.ADAMS_LAUNCH_COMMAND = TEST_GOOD_CMD_2
        os.environ['ADAMS_LAUNCH_COMMAND'] = str(TEST_GOOD_CMD_3)

    def test_argument(self):
        cmd = adams_bin_converter._get_adams_launch_command(TEST_GOOD_CMD_1)
        self.assertEqual(cmd, TEST_GOOD_CMD_1)

    def test_no_argument(self):
        cmd = adams_bin_converter._get_adams_launch_command()
        self.assertEqual(cmd, TEST_GOOD_CMD_2)

    def tearDown(self):
        return
    
class Test_GoodmvNoev(unittest.TestCase):

    def setUp(self):
        adams_bin_converter.ADAMS_LAUNCH_COMMAND = TEST_GOOD_CMD_2
        _ = os.environ.pop('ADAMS_LAUNCH_COMMAND')

    def test_argument(self):
        cmd = adams_bin_converter._get_adams_launch_command(TEST_GOOD_CMD_1)
        self.assertEqual(cmd, TEST_GOOD_CMD_1)

    def test_no_argument(self):
        cmd = adams_bin_converter._get_adams_launch_command()
        self.assertEqual(cmd, TEST_GOOD_CMD_2)

    def tearDown(self):
        return
    
class Test_NomvGoodev(unittest.TestCase):

    def setUp(self):
        os.environ['ADAMS_LAUNCH_COMMAND'] = str(TEST_GOOD_CMD_3)

    def test_argument(self):
        cmd = adams_bin_converter._get_adams_launch_command(TEST_GOOD_CMD_1)
        self.assertEqual(cmd, TEST_GOOD_CMD_1)

    def test_no_argument(self):
        cmd = adams_bin_converter._get_adams_launch_command()
        self.assertEqual(cmd, TEST_GOOD_CMD_3)

    def tearDown(self):
        return
    
class Test_NomvNoev(unittest.TestCase):

    def setUp(self):
        _ = os.environ.pop('ADAMS_LAUNCH_COMMAND')

    def test_argument(self):
        cmd = adams_bin_converter._get_adams_launch_command(TEST_GOOD_CMD_1)
        self.assertEqual(cmd, TEST_GOOD_CMD_1)

    def test_no_argument(self):
        with self.assertRaises(EnvironmentError):
            cmd = adams_bin_converter._get_adams_launch_command()

    def tearDown(self):
        return
    
class Test_GoodmvBadev(unittest.TestCase):

    def setUp(self):
        adams_bin_converter.ADAMS_LAUNCH_COMMAND = TEST_GOOD_CMD_2
        os.environ['ADAMS_LAUNCH_COMMAND'] = str(TEST_BAD_CMD)

    def test_argument(self):
        cmd = adams_bin_converter._get_adams_launch_command(TEST_GOOD_CMD_1)
        self.assertEqual(cmd, TEST_GOOD_CMD_1)

    def test_no_argument(self):
        cmd = adams_bin_converter._get_adams_launch_command()
        self.assertEqual(cmd, TEST_GOOD_CMD_2)

    def tearDown(self):
        return
    
class Test_BadmvGoodev(unittest.TestCase):

    def setUp(self):
        adams_bin_converter.ADAMS_LAUNCH_COMMAND = TEST_BAD_CMD
        os.environ['ADAMS_LAUNCH_COMMAND'] = str(TEST_GOOD_CMD_3)

    def test_argument(self):
        cmd = adams_bin_converter._get_adams_launch_command(TEST_GOOD_CMD_1)
        self.assertEqual(cmd, TEST_GOOD_CMD_1)

    def test_no_argument(self):
        cmd = adams_bin_converter._get_adams_launch_command()
        self.assertEqual(cmd, TEST_GOOD_CMD_3)

    def tearDown(self):
        return
    
class Test_BadmvBadev(unittest.TestCase):

    def setUp(self):
        adams_bin_converter.ADAMS_LAUNCH_COMMAND = TEST_BAD_CMD
        os.environ['ADAMS_LAUNCH_COMMAND'] = str(TEST_BAD_CMD)

    def test_argument(self):
        cmd = adams_bin_converter._get_adams_launch_command(TEST_GOOD_CMD_1)
        self.assertEqual(cmd, TEST_GOOD_CMD_1)

    def test_no_argument(self):
        with self.assertRaises(EnvironmentError):
            cmd = adams_bin_converter._get_adams_launch_command()

    def tearDown(self):
        return