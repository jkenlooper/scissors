from bs4 import BeautifulSoup
import svgwrite

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

    def __init__(self, svgfile=None, svgstring=None):
        """
        Parse the svg paths document into individual clipPaths by finding
        elements set to the marker class.
        """
        # create a soup from reading in the svgfile
        if (svgfile):
            self._soup = BeautifulSoup(open(svgfile))
        elif (svgstring):
            self._soup = BeautifulSoup(svgstring)
        else:
            raise ValueError('no svg specified')

        # get the dimensions from svgfile
        svg = self._soup.svg
        self._width = svg.get('width', '100%')
        self._height = svg.get('height', '100%')

        # find all elements with the clip classname? not always possible to be
        # able to add a class name to elements using wysiwyg type editors.
        #TODO: consider each top level element to be a 'layer' or clip
        for svg_clip in svg.find_all(self._tags, recursive=False):
            dwg = svgwrite.Drawing(size=(self._width, self._height), profile='full')
            dwg.set_desc(title="Scissors Clip", desc="")

            #add the defs element
            clip_path = dwg.defs.add(dwg.clipPath())
            clip_path['id'] = 'clip_path'
            
            


            right_path = clip_path.add(
                    dwg.path('M 250 0 L 250 250 L 200 300 L 500 500 L 500 0')
                    )
            #right_path['clip-rule'] = 'evenodd'
            #clip_down_center.add(dwg.line((250,0), (250,500)))
            clip_path.add(dwg.circle((200,20), 150))

            test_rect = dwg.defs.add(
                    dwg.rect((50,50), (400,400), fill="blue", id="test_rect")
                    )

            #dwg.defs.add(clip_down_center)

            #test_rect = dwg.rect((50,50), (100,100))
            g = dwg.add(dwg.g())
            inserted_test_rect = g.add(dwg.use(test_rect, insert=(0,0)))
            inserted_test_rect['clip-path'] = 'url(#clip_path)'
            #test_rect['clip-path'] = '#clip_down_center'
            #dwg.add(test_rect)

            dwg.save()


        # create svgfile using svgwrite for each

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
