import os
import subprocess

from bs4 import BeautifulSoup
from pgmagick import Image, CompositeOperator as co
import svgwrite

class Clips(object):
    """
    Contains reference to all the clips created from a svg file.
    Clips could be used on multiple images.
    """
    #clip_classname = 'clip'
    #group_classname = 'clip-group'

    masks = []

    _soup = None
    _tags = (
            'line',
            'rect',
            'circle',
            'ellipse',
            'polyline',
            'polygon',
            'text',
            'tspan',
            'tref',
            'textPath',
            'textArea',
            'path',
            'image',
            'g',
            'symbol',
            'linearGradient',
            'radialGradient',
            'mask',
            'clipPath',
            )

    def __init__(self, svgfile=None, svgstring=None, clips_dir='',
            dimensions=None, pretty=True):
        #TODO: dimensions can be used to create a clips that is smaller/larger
        # then what the svgfile is set to.
        self._clip_counter = 0
        self.clips_dir = clips_dir
        self.pretty = pretty
        # create a soup from reading in the svgfile
        if (svgfile):
            self._soup = BeautifulSoup(open(svgfile), 'xml')
        elif (svgstring):
            self._soup = BeautifulSoup(svgstring, 'xml')
        else:
            raise ValueError('no svg specified')
        self._create_clip_svgs()
        self._rasterize_clips()
        self._composite_clips()

    def _create_clip_svgs(self):
        """
        Parse the svg file or string into individual clipPaths by finding
        elements at the top level.
        """
        # get the dimensions from svgfile
        svg = self._soup.svg
        self._width = svg.get('width', '100%')
        self._height = svg.get('height', '100%')

        # find all elements with the clip classname? not always possible to be
        # able to add a class name to elements using wysiwyg type editors.
        #TODO: consider each top level element to be a 'layer' or clip
        for svg_clip in svg.find_all(self._tags, recursive=False):
            # create a blank 'paper' ready to be clipped.
            dwg = svgwrite.Drawing(size=(self._width, self._height), profile='full')
            dwg.set_desc(title="Scissors Clip", desc="")

            clip_path = dwg.defs.add(dwg.clipPath())
            clip_path['id'] = 'clip_path'

            paper_rect = dwg.defs.add(
                    dwg.rect((0,0), (self._width, self._height), fill="black",
                        id="scissors_paper_rect")
                    )
            g = dwg.add(dwg.g())
            g.add(dwg.use(paper_rect, insert=(0,0), clip_path='url(#clip_path)'))

            #read in paper to soup
            paper_soup = BeautifulSoup(dwg.tostring(), 'xml')
            #append svg_clip to clip_path
            clip_path = paper_soup.find(id='clip_path')
            clip_path.append(svg_clip)

            # strip out any stuff that we don't need
            # or add the xmlns?

            f = open(os.path.join(self.clips_dir, 'clip-%i.svg' %
                self._clip_counter), 'w')
            if self.pretty:
                f.write(paper_soup.prettify())
            else:
                f.write(unicode(paper_soup))
            f.close()
            self._clip_counter = self._clip_counter + 1

        self.count = self._clip_counter


    def _rasterize_clips(self):
        """
        Converts clip-X.svg to clip-X.png which has an alpha channel where each
        clip is.
        """
        raster = ['/usr/bin/java', '-Xint', '-jar']

        #TODO: better way of getting the path to the rasterizer?
        raster.append('batik-1.7/batik-rasterizer.jar')

        for clip_number in range(0, self.count):
            raster.append(os.path.join(self.clips_dir, 'clip-%i.svg' % clip_number))

        subprocess.call(raster, shell=False)

    def _composite_clips(self):
        """
        for each rasterized clip subtract the alpha from the previous.
        """
        #skip the first clip as it doesn't need anything taken away from it.
        this_clip = Image(os.path.join(self.clips_dir, 'clip-0.png'))
        this_clip.write(os.path.join(self.clips_dir, "clip-co-0.png"))
        self.masks.append(os.path.join(self.clips_dir, 'clip-co-0.png'))

        for clip_number in range(1, self.count):
            previous_clip = Image(os.path.join(self.clips_dir, 'clip-%i.png' %
                int(clip_number-1)))
            this_clip = Image(os.path.join(self.clips_dir, 'clip-%i.png' %
                clip_number))

            this_clip.composite(previous_clip, 0, 0, co.XorCompositeOp)
            this_clip.write(os.path.join(self.clips_dir, "clip-co-%i.png" % clip_number))
            self.masks.append(os.path.join(self.clips_dir, 'clip-co-%i.png' % clip_number))


class Scissors(object):
    """

    """

    def __init__(self, clips, image, target_directory):
        """
        Init with a clips object, image, and target directory.
        """
        self.image = image
        self.clips = clips
        self.target_directory = target_directory

    def cut(self):
        """
        """
        #TODO: multi-dimensional clips
        # for each clip; clip the image and place in target_directory
        for clip_mask in self.clips.masks:
            self._composite(clip_mask, self.image)


    def _composite(self, mask, pic):
        """
        composite of mask and pic.
        """
        base = Image(pic)
        layer = Image(mask) 
        # anything that is opaque(black) in the layer will be cut. The rest
        # will be discarded.
        base.composite(layer, 0, 0, co.CopyOpacityCompositeOp)
        base.write(os.path.join(self.target_directory, "%s-%s.png" %
            (os.path.basename(pic), os.path.basename(mask))))

        # make a new clip image
        #out = Image('out.png')
        #base = Image(pic)
        #base.composite(out, 100, 0, co.CopyOpacityCompositeOp)
        #base.write('out2.png')

