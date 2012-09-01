from bs4 import BeautifulSoup
from pgmagick import Image, CompositeOperator as co
import svgwrite
import os

class Clips(object):
    """
    Contains reference to all the clips created from a svg file.
    """
    #clip_classname = 'clip'
    #group_classname = 'clip-group'

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
            pretty=True):
        """
        Parse the svg paths document into individual clipPaths by finding
        elements at the top level.
        """
        # create a soup from reading in the svgfile
        if (svgfile):
            self._soup = BeautifulSoup(open(svgfile), 'xml')
        elif (svgstring):
            self._soup = BeautifulSoup(svgstring, 'xml')
        else:
            raise ValueError('no svg specified')

        self._clip_counter = 0
        self.clips_dir = clips_dir

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
            if pretty:
                f.write(paper_soup.prettify())
            else:
                f.write(unicode(paper_soup))
            f.close()



class Scissors(object):
    """

    """

    def __init__(self, clips, image, target_directory):
        """
        Init with a clips object, image, and target directory.
        """

    def cut(self):
        """
        """

    def _rasterize_clip(self, clip):
        """
        Create a mask (black and white image) from the clip.
        """

    def _composite(self, mask, pic):
        """
        composite of mask and pic.
        """
        base = Image(pic)
        layer = Image(mask) 
        # anything that is opaque(black) in the layer will be cut. The rest
        # will be discarded.
        base.composite(layer, 0, 0, co.CopyOpacityCompositeOp)
        base.write('out.png')

        # make a new clip image
        out = Image('out.png')
        base = Image(pic)
        base.composite(out, 100, 0, co.CopyOpacityCompositeOp)
        base.write('out2.png')

