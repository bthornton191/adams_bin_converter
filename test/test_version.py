import unittest

from adams_bin_converter import ADAMS_INSTALL_DIR, AdamsVersionError, Version
from test import TEST_FILE_DIR_SINGLE

TEST_BIN_FILE = TEST_FILE_DIR_SINGLE / 'test_1.bin'



TEST_AVAILABLE_VERSIONS = [
    Version(year=2015, release=1, update=0, build=0, other=[]),
    Version(year=2018, release=1, update=0, build=0, other=[]),
    Version(year=2019, release=2, update=0, build=0, other=[]),
    Version(year=2019, release=2, update=1, build=0, other=[]),
    Version(year=2020, release=1, update=0, build=748966, other=[]),
    Version(year=2020, release=0, update=0, build=711253, other=[]),
    Version(year=2021, release=0, update=1, build=784690, other=[]),
    Version(year=2021, release=1, update=0, build=801488, other=[]),
    Version(year=2021, release=2, update=2, build=826892, other=[]),
]

class Test_Version(unittest.TestCase):

    def setUp(self):
        return

    def test_version_from_bin_file(self):
        expected_ver = Version(2018,1)
        ver = Version.from_bin_file(TEST_BIN_FILE)

        self.assertEqual(ver, expected_ver)

    def test_version_from_install_dir(self):
        instal_dir = Version.get_installed_version_dirs(ADAMS_INSTALL_DIR)[0]
        expected_ver = Version(2015,1)
        ver = Version.from_install_dir(instal_dir)

        self.assertEqual(ver, expected_ver)

    def tearDown(self):
        return

class Test_VersionFinder(unittest.TestCase):

    def setUp(self):
        return

    def test_version_multiple_year_match_single_release_match_single_update_match(self):
        """Returned version should match year, release, and update when looking for a version whose 
        year matches multiple, releases matches one, and update matches one.
        """
        comps_to_match = ['year', 'release', 'update']
        tgt = Version(2021, 1, 0, 0)
        act = tgt.get_closest_version(TEST_AVAILABLE_VERSIONS)
        self.assertTrue(all([getattr(tgt, comp) == getattr(act, comp) for comp in comps_to_match]))

    def test_version_multiple_year_match_multiple_release_match_single_update_match(self):
        """Returned version should match year, release, and update when looking for a version whose 
        year matches multiple, releases matches multiple, and update matches one.
        """
        comps_to_match = ['year', 'release', 'update']
        tgt = Version(2019, 2, 0, 0)
        act = tgt.get_closest_version(TEST_AVAILABLE_VERSIONS)
        self.assertTrue(all([getattr(tgt, comp) == getattr(act, comp) for comp in comps_to_match]))

    def test_version_multiple_year_match_multiple_release_match_no_update_match(self):
        """Returned version should match year, release, and update when looking for a version whose 
        year matches multiple, releases matches multiple, and update matches NONE.
        """
        comps_to_match = ['year', 'release']
        comps_to_not_match = ['update']
        tgt = Version(2019, 2, 3, 0)
        act = tgt.get_closest_version(TEST_AVAILABLE_VERSIONS)
        
        tests = [getattr(tgt, comp) == getattr(act, comp) for comp in comps_to_match]
        tests += [getattr(tgt, comp) != getattr(act, comp) for comp in comps_to_not_match]
        self.assertTrue(all(tests))

    def test_version_multiple_year_no_other_matches(self):
        """Returned version should match year, release, and update when looking for a version whose 
        year matches multiple, but nothing else matches.
        """
        comps_to_match = ['year']
        comps_to_not_match = ['release', 'update', 'build']
        tgt = Version(2021, 3, 4, 561566)
        act = tgt.get_closest_version(TEST_AVAILABLE_VERSIONS)

        tests = [getattr(tgt, comp) == getattr(act, comp) for comp in comps_to_match]
        tests += [getattr(tgt, comp) != getattr(act, comp) for comp in comps_to_not_match]
        self.assertTrue(all(tests))

    def test_version_multiple_no_matching_year_but_following_year_available(self):
        """Returned version should have a year that is greater than the target when looking for a 
        version that doesn't exist, but there is a later version available.
        """
        tgt = Version(2016, 3, 4, 561566)
        act = tgt.get_closest_version(TEST_AVAILABLE_VERSIONS)
        
        tests = [act.year > tgt.year]
        self.assertTrue(all(tests))

    def test_version_multiple_no_matching_year_but_following_year_available(self):
        """Raises an AdamsVersionError when looking for a version that doesn't exist and there is no
        later version that exists.
        """
        tgt = Version(2022, 3, 4, 561566)
        with self.assertRaises(AdamsVersionError):
            tgt.get_closest_version(TEST_AVAILABLE_VERSIONS)

    def tearDown(self):
        return