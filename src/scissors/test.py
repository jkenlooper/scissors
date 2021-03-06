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
        dwg.viewbox(width=1280, height=960)
        dwg.stretch()
        dwg.set_desc(title="Scratch drawing", desc="Just testing")
        return dwg

    def tearDown(self):
        """Get rid of files."""
        # don't want to do that just yet.
        pass

class SimpleCuts(Mixin, unittest.TestCase):

    def test_one_vertical(self):
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
                clips_dir=os.path.join(self.test_dir, sub_dir),
                size=(1280, 960))

        scissors = Scissors(clips, 'wild-daisy.jpg',
                os.path.join(self.test_dir, sub_dir))
        scissors.cut()

    def test_two_vertical(self):
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
                clips_dir=os.path.join(self.test_dir, sub_dir),
                size=(1280, 960))

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
                clips_dir=os.path.join(self.test_dir, sub_dir),
                size=(1280, 960))

        scissors = Scissors(clips, 'wild-daisy.jpg',
                os.path.join(self.test_dir, sub_dir))
        scissors.cut()

class DoubleCuts(Mixin, unittest.TestCase):

    def test_three_and_one(self):
        """Three vertical cut and one horizontal"""
        sub_dir = 'test_three_and_one'
        self._create_empty_dir(sub_dir)

        dwg = self._scratch_drawing()

        layer1 = dwg.add(dwg.g())
        g1 = layer1.add(dwg.g())
        simple_path_down_center = g1.add(
                dwg.path('M 0 0 L 250 0 L 200 300 L 250 960 L 0 960')
                )
        g2 = layer1.add(dwg.g())
        simple_path_down_center = g2.add(
                dwg.path('M 0 0 L 450 0 L 480 200 L 450 960 L 0 960')
                )

        g3 = layer1.add(dwg.g())
        simple_path_down_center = g3.add(
                dwg.path('M 0 0 L 650 0 L 680 400 L 650 960 L 0 960')
                )

        # layer 2
        layer2 = dwg.add(dwg.g())
        g1 = layer2.add(dwg.g())
        simple_path = g1.add(
                dwg.path('M 0 0 L 1280 0 L 1280 200 L 600 360 L 0 200')
                )

        clips = Clips(svgstring=dwg.tostring(),
                clips_dir=os.path.join(self.test_dir, sub_dir),
                size=(1280, 960))

        scissors = Scissors(clips, 'wild-daisy.jpg',
                os.path.join(self.test_dir, sub_dir))
        scissors.cut()

    def test_three_and_two(self):
        """Three vertical cut and two horizontal"""
        sub_dir = 'test_three_and_two'
        self._create_empty_dir(sub_dir)

        dwg = self._scratch_drawing()

        layer1 = dwg.add(dwg.g())
        g1 = layer1.add(dwg.g())
        simple_path_down_center = g1.add(
                dwg.path('M 0 0 L 250 0 L 200 300 L 250 960 L 0 960')
                )
        g2 = layer1.add(dwg.g())
        simple_path_down_center = g2.add(
                dwg.path('M 0 0 L 450 0 L 480 200 L 450 960 L 0 960')
                )

        g3 = layer1.add(dwg.g())
        simple_path_down_center = g3.add(
                dwg.path('M 0 0 L 650 0 L 680 400 L 650 960 L 0 960')
                )

        # layer 2
        layer2 = dwg.add(dwg.g())
        g1 = layer2.add(dwg.g())
        simple_path = g1.add(
                dwg.path('M 0 0 L 1280 0 L 1280 200 L 600 360 L 0 200')
                )

        g2 = layer2.add(dwg.g())
        simple_path = g2.add(
                dwg.path('M 0 0 L 1280 0 L 1280 400 L 300 560 L 0 500')
                )

        clips = Clips(svgstring=dwg.tostring(),
                clips_dir=os.path.join(self.test_dir, sub_dir),
                size=(1280, 960))

        scissors = Scissors(clips, 'wild-daisy.jpg',
                os.path.join(self.test_dir, sub_dir))
        scissors.cut()

    def test_three_and_three(self):
        """Three vertical cut and three horizontal"""
        sub_dir = 'test_three_and_three'
        self._create_empty_dir(sub_dir)

        dwg = self._scratch_drawing()

        layer1 = dwg.add(dwg.g())
        g1 = layer1.add(dwg.g())
        simple_path_down_center = g1.add(
                dwg.path('M 0 0 L 250 0 L 200 300 L 250 960 L 0 960')
                )
        g2 = layer1.add(dwg.g())
        simple_path_down_center = g2.add(
                dwg.path('M 0 0 L 450 0 L 480 200 L 450 960 L 0 960')
                )

        g3 = layer1.add(dwg.g())
        simple_path_down_center = g3.add(
                dwg.path('M 0 0 L 650 0 L 680 400 L 650 960 L 0 960')
                )

        # layer 2
        layer2 = dwg.add(dwg.g())
        g1 = layer2.add(dwg.g())
        simple_path = g1.add(
                dwg.path('M 0 0 L 1280 0 L 1280 200 L 600 360 L 0 200')
                )

        g2 = layer2.add(dwg.g())
        simple_path = g2.add(
                dwg.path('M 0 0 L 1280 0 L 1280 400 L 300 560 L 0 500')
                )

        g3 = layer2.add(dwg.g())
        simple_path = g3.add(
                dwg.path('M 0 0 L 1280 0 L 1280 600 L 900 760 L 0 600')
                )

        clips = Clips(svgstring=dwg.tostring(),
                clips_dir=os.path.join(self.test_dir, sub_dir),
                size=(1280, 960))

        scissors = Scissors(clips, 'wild-daisy.jpg',
                os.path.join(self.test_dir, sub_dir))
        scissors.cut()

class SmallCuts(Mixin, unittest.TestCase):

    def test_three_and_three(self):
        """smaller Three vertical cut and three horizontal"""
        sub_dir = 'test_smaller_three_and_three'
        self._create_empty_dir(sub_dir)

        dwg = self._scratch_drawing()

        layer1 = dwg.add(dwg.g())
        g1 = layer1.add(dwg.g())
        simple_path_down_center = g1.add(
                dwg.path('M 0 0 L 250 0 L 200 300 L 250 960 L 0 960')
                )
        g2 = layer1.add(dwg.g())
        simple_path_down_center = g2.add(
                dwg.path('M 0 0 L 450 0 L 480 200 L 450 960 L 0 960')
                )

        g3 = layer1.add(dwg.g())
        simple_path_down_center = g3.add(
                dwg.path('M 0 0 L 650 0 L 680 400 L 650 960 L 0 960')
                )

        # layer 2
        layer2 = dwg.add(dwg.g())
        g1 = layer2.add(dwg.g())
        simple_path = g1.add(
                dwg.path('M 0 0 L 1280 0 L 1280 200 L 600 360 L 0 200')
                )

        g2 = layer2.add(dwg.g())
        simple_path = g2.add(
                dwg.path('M 0 0 L 1280 0 L 1280 400 L 300 560 L 0 500')
                )

        g3 = layer2.add(dwg.g())
        simple_path = g3.add(
                dwg.path('M 0 0 L 1280 0 L 1280 600 L 900 760 L 0 600')
                )

        clips = Clips(svgstring=dwg.tostring(),
                clips_dir=os.path.join(self.test_dir, sub_dir),
                size=(256, 192))

        #wild-daisy-small.jpg = 256x192
        scissors = Scissors(clips, 'wild-daisy-small.jpg',
                os.path.join(self.test_dir, sub_dir))
        scissors.cut()

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SimpleCuts))
    #add others
    return suite


if __name__ == '__main__':
    unittest.main()

