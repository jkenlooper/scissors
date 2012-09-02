# test for image cut into two pieces vertically

import os.path
import unittest

import svgwrite

from scissors.base import Clips, Scissors

#import scissors.

class Mixin(object):
    def setUp(self):
        """Before each test, set up the scissors"""

    def tearDown(self):
        """Get rid of the database again after each test."""
        pass

class SimpleCuts(Mixin, unittest.TestCase):

    def test_one_vertical(self):
        """A single vertical cut"""
        dwg = svgwrite.Drawing(size=(500,500), profile='full')
        dwg.set_desc(title="Scratch drawing", desc="Just testing")

        g = dwg.add(dwg.g())
        #g['class'] = 'clip'
        simple_path_down_center = g.add(
                dwg.path('M 0 0 L 250 0 L 200 300 L 250 500 L 0 500')
                )
        clips = Clips(svgstring=dwg.tostring())

        scissors = Scissors(clips, 'wild-daisy.jpg', 'test')
        scissors.cut()


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SimpleCuts))
    #add others
    return suite


if __name__ == '__main__':
    unittest.main()

