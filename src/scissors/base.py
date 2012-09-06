import os
import subprocess
from tempfile import SpooledTemporaryFile

from bs4 import BeautifulSoup
from pgmagick import Image, CompositeOperator as co
import svgwrite

class Clips(object):
    """
    Contains reference to all the clips created from a svg file.
    Clips could be used on multiple images.
    """

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
            size=None, pretty=True):
        self._clip_counter = 0
        self.masks = []
        self._clip_layers = []
        self.size = size

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
        if self.size:
            self._width = self.size[0]
            self._height = self.size[1]
        else:
            self._width = svg.get('width', '100%')
            self._height = svg.get('height', '100%')
        vb = svg.get('viewBox', None)

        # find all elements with the clip classname? not always possible to be
        # able to add a class name to elements using wysiwyg type editors.
        for layer in svg.find_all('g', recursive=False):
            clips = []
            for svg_clip in layer.find_all(self._tags, recursive=False):
                # create a blank 'paper' ready to be clipped.
                dwg = svgwrite.Drawing(size=(self._width, self._height), profile='full')
                if vb: # TODO: better way of doing this?
                    (minx, miny, width, height) = vb.split(',') # could also be separated by spaces?
                    dwg.viewbox(width=width, height=height)
                    dwg.stretch() # assume that we always want to do this for now.
                dwg.set_desc(title="Scissors Clip", desc="")

                clip_path = dwg.defs.add(dwg.clipPath())
                clip_path['id'] = 'clip_path'

                paper_rect = dwg.defs.add(
                        dwg.rect((0,0), (width, height), fill="black",
                            id="scissors_paper_rect")
                        )
                g = dwg.add(dwg.g())
                g.add(dwg.use(paper_rect, insert=(0,0), clip_path='url(#clip_path)'))

                #read in paper to soup
                paper_soup = BeautifulSoup(dwg.tostring(), 'xml')
                #append svg_clip to clip_path
                clip_path = paper_soup.find(id='clip_path')
                clip_path.append(svg_clip)

                #TODO: strip out any stuff that we don't need
                # or add the xmlns?

                clip_id = '%i-%i' % (len(clips), len(self._clip_layers))

                f = open(os.path.join(self.clips_dir, 'clip-%s.svg' % clip_id), 'w')
                if self.pretty:
                    f.write(paper_soup.prettify())
                else:
                    f.write(unicode(paper_soup))
                f.close()
                #self._clip_counter = self._clip_counter + 1
                clips.append(clip_id)
            self._clip_layers.append(clips)

        #self.count = self._clip_counter


    def _rasterize_clips(self):
        """
        Converts clip-X.svg to clip-X.png which has an alpha channel where each
        clip is.
        """
        raster = ['/usr/bin/java', '-Xint', '-jar']

        #TODO: better way of getting the path to the rasterizer?
        raster.append('batik-1.7/batik-rasterizer.jar')

        for clips in self._clip_layers:
            for clip_id in clips:
                raster.append(os.path.join(self.clips_dir, 'clip-%s.svg' % clip_id))

        subprocess.call(raster, shell=False)

    def _composite_clips(self):
        """
        for each rasterized clip subtract the alpha from the previous.
        """
        for clips in self._clip_layers:
            layer_level = 0
            self._xor_composite_clip_layer(clips, layer_level=layer_level)
            layer_level = layer_level + 1

        if len(self._clip_layers) == 1:
            for clip_id in self._clip_layers[0]:
                self.masks.append(os.path.join(self.clips_dir, 'clip-co-%s.png'
                    % clip_id))
        count = 0
        for clips in self._clip_layers[1:]:
            self._in_composite(self._clip_layers[count], clips)
            count = count + 1


    def _xor_composite_clip_layer(self, clips, layer_level=0):
        """
        round two clipping.
        """

        #skip the first clip as it doesn't need anything taken away from it.
        this_clip = Image(os.path.join(self.clips_dir, 'clip-%s.png' %
            clips[0]))
        this_clip.write(os.path.join(self.clips_dir, "clip-co-%s.png" %
            clips[0]))
        #self.masks.append(os.path.join(self.clips_dir, 'clip-co-%s.png' %
            #clips[0]))

        clip_i = 0
        for clip_id in clips[1:]:
            previous_clip = Image(os.path.join(self.clips_dir, 'clip-%s.png' %
                clips[clip_i]))
            this_clip = Image(os.path.join(self.clips_dir, 'clip-%s.png' %
                clip_id))

            this_clip.composite(previous_clip, 0, 0, co.XorCompositeOp)
            #TODO: verify that clip still has some pixels
            this_clip.write(os.path.join(self.clips_dir, "clip-co-%s.png" %
                clip_id))
            clip_i = clip_i + 1

    def _in_composite(self, previous_clips, clips):
        for prev_clip_id in previous_clips:
            for this_clip_id in clips:
                previous_clip = Image(os.path.join(self.clips_dir, 'clip-co-%s.png' %
                    prev_clip_id))
                this_clip = Image(os.path.join(self.clips_dir, 'clip-co-%s.png' %
                    this_clip_id))

                this_clip.composite(previous_clip, 0, 0, co.InCompositeOp)
                #TODO: verify that clip still has some pixels
                this_clip.write(os.path.join(self.clips_dir, "clip-in-%s-%s.png" %
                    (prev_clip_id, this_clip_id)))
                self.masks.append(os.path.join(self.clips_dir, 'clip-in-%s-%s.png'
                    % (prev_clip_id, this_clip_id)))



class Scissors(object):
    """
    Cuts up images based on the clips.
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
        Cut the image up in pieces.
        """
        for clip_mask in self.clips.masks:
            self._composite(clip_mask, self.image)


    def _composite(self, mask, pic):
        """
        composite of mask and pic. also trims it and renames with offset.
        """
        base = Image(pic)
        layer = Image(mask) 
        base.composite(layer, 0, 0, co.CopyOpacityCompositeOp)
        finished_clip_filename = os.path.join(self.target_directory, "%s-%s.png" %
            (os.path.basename(pic), os.path.basename(mask)))
        base.write(finished_clip_filename)

        # Use imagemagick here, since gm doesn't show offset info (geometry)
        # after trim.

        #mogrify -trim image.png
        m = subprocess.call(['mogrify', '-trim', finished_clip_filename])

        #identify -ping -format '%w-%h-%g' image.png
        # example: 214-219-1280x960+461+499
        f = SpooledTemporaryFile()
        i = subprocess.call(['identify', '-ping', '-format', '%w-%h-%g',
            finished_clip_filename], stdout=f)
        f.seek(0)
        d = f.read()
        d = d.strip()
        (root, ext) = os.path.splitext(finished_clip_filename)
        new_name = '%s_%s%s' % (root, d, ext)
        os.rename(finished_clip_filename, new_name)
