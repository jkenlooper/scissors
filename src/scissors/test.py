# test for image cut into two pieces vertically

import os, glob
import os.path
import unittest

import svgwrite

from scissors.base import Clips, Scissors

#import scissors.

class Mixin(object):
    test_dir = 'test'

    def setUp(self):
        """Before testing setup"""

    def _create_empty_dir(self, sub_dir):
        """Before each test, create an empty test directory"""
        print 'setup: %s' % sub_dir
        try:
            for p in glob.glob(os.path.join(self.test_dir, sub_dir, '*')):
                os.unlink(p)
            os.rmdir(os.path.join(self.test_dir, sub_dir))
        except OSError:
            pass
        os.mkdir(os.path.join(self.test_dir, sub_dir))

    def _scratch_drawing(self):
        dwg = svgwrite.Drawing(size=(1280,960), profile='full')
        dwg.set_desc(title="Scratch drawing", desc="Just testing")
        return dwg

    def tearDown(self):
        """Get rid of files."""
        # don't want to do that just yet.
        pass

class SimpleCuts(Mixin, unittest.TestCase):

    def _test_one_vertical(self):
        """A single vertical cut"""
        sub_dir = 'test_one_vertical'
        self._create_empty_dir(sub_dir)

        dwg = self._scratch_drawing()

        layer = dwg.add(dwg.g())
        g = layer.add(dwg.g())
        #g['class'] = 'clip'
        simple_path_down_center = g.add(
                dwg.path('M 0 0 L 250 0 L 200 300 L 250 960 L 0 960')
                )
        clips = Clips(svgstring=dwg.tostring(),
                clips_dir=os.path.join(self.test_dir, sub_dir))

        scissors = Scissors(clips, 'wild-daisy.jpg',
                os.path.join(self.test_dir, sub_dir))
        scissors.cut()

    def _test_two_vertical(self):
        """Two vertical cuts"""
        sub_dir = 'test_two_vertical'
        self._create_empty_dir(sub_dir)

        dwg = self._scratch_drawing()

        layer = dwg.add(dwg.g())
        g1 = layer.add(dwg.g())
        simple_path_down_center = g1.add(
                dwg.path('M 0 0 L 250 0 L 200 300 L 250 960 L 0 960')
                )
        g2 = layer.add(dwg.g())
        simple_path_down_center = g2.add(
                dwg.path('M 0 0 L 450 0 L 480 200 L 450 960 L 0 960')
                )

        clips = Clips(svgstring=dwg.tostring(),
                clips_dir=os.path.join(self.test_dir, sub_dir))

        scissors = Scissors(clips, 'wild-daisy.jpg',
                os.path.join(self.test_dir, sub_dir))
        scissors.cut()

    def test_three_vertical(self):
        """Three vertical cuts"""
        sub_dir = 'test_three_vertical'
        self._create_empty_dir(sub_dir)

        dwg = self._scratch_drawing()

        layer = dwg.add(dwg.g())
        g1 = layer.add(dwg.g())
        simple_path_down_center = g1.add(
                dwg.path('M 0 0 L 250 0 L 200 300 L 250 960 L 0 960')
                )
        g2 = layer.add(dwg.g())
        simple_path_down_center = g2.add(
                dwg.path('M 0 0 L 450 0 L 480 200 L 450 960 L 0 960')
                )

        g3 = layer.add(dwg.g())
        simple_path_down_center = g3.add(
                dwg.path('M 0 0 L 650 0 L 680 400 L 650 960 L 0 960')
                )

        clips = Clips(svgstring=dwg.tostring(),
                clips_dir=os.path.join(self.test_dir, sub_dir))

        scissors = Scissors(clips, 'wild-daisy.jpg',
                os.path.join(self.test_dir, sub_dir))
        scissors.cut()

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SimpleCuts))
    #add others
    return suite


if __name__ == '__main__':
    unittest.main()

