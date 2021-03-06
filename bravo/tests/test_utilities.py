# vim: set fileencoding=utf8 :

import unittest

from numpy import array
from numpy.testing import assert_array_equal

from bravo.utilities.bits import unpack_nibbles, pack_nibbles
from bravo.utilities.chat import sanitize_chat
from bravo.utilities.coords import split_coords, taxicab2, taxicab3
from bravo.utilities.temporal import split_time

class TestCoordHandling(unittest.TestCase):

    def test_split_coords(self):
        cases = {
            (0, 0): (0, 0, 0, 0),
            (1, 1): (0, 1, 0, 1),
            (16, 16): (1, 0, 1, 0),
            (-1, -1): (-1, 15, -1, 15),
            (-16, -16): (-1, 0, -1, 0),
        }
        for case in cases:
            self.assertEqual(split_coords(*case), cases[case])

    def test_taxicab2(self):
        cases = {
            (1, 2, 3, 4): 4,
            (1, 2, 1, 2): 0,
            (2, 1, 4, 3): 4,
        }
        for case in cases:
            self.assertEqual(taxicab2(*case), cases[case])

    def test_taxicab3(self):
        cases = {
            (1, 2, 1, 3, 4, 2): 5,
            (1, 2, 3, 1, 2, 3): 0,
            (2, 1, 2, 4, 3, 1): 5,
        }
        for case in cases:
            self.assertEqual(taxicab3(*case), cases[case])

class TestBitTwiddling(unittest.TestCase):

    def test_unpack_nibbles(self):
        assert_array_equal(unpack_nibbles("a"), [1, 6])
        assert_array_equal(unpack_nibbles("nibbles"),
            [14, 6, 9, 6, 2, 6, 2, 6, 12, 6, 5, 6, 3, 7])

    def test_pack_nibbles(self):
        self.assertEqual(pack_nibbles(array([1, 6])), "a")
        self.assertEqual(
            pack_nibbles(array([14, 6, 9, 6, 2, 6, 3, 7])),
            "nibs")

    def test_nibble_reflexivity(self):
        self.assertEqual("nibbles",
            pack_nibbles(
                array(unpack_nibbles("nibbles"))
            )
        )

    def test_unpack_nibbles_overflow(self):
        """
        No spurious OverflowErrors should occur when packing nibbles.

        This test doesn't even assert anything; it will raise instead if
        there's a regression.
        """

        pack_nibbles(array([0xff, 0xff]))

class TestStringMunging(unittest.TestCase):

    def test_sanitize_chat_color_control_at_end(self):
        message = u"§0Test§f"
        sanitized = u"§0Test"
        self.assertEqual(sanitize_chat(message), sanitized)

class TestNumberMunching(unittest.TestCase):

    def test_split_time(self):
        # Sunrise.
        self.assertEqual(split_time(0), (6, 0))
        # Noon.
        self.assertEqual(split_time(6000), (12, 0))
        # Sunset.
        self.assertEqual(split_time(12000), (18, 0))
        # Midnight.
        self.assertEqual(split_time(18000), (0, 0))
