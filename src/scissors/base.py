import os
import subprocess
import json

from bs4 import BeautifulSoup
from pgmagick import Image as GMImage, CompositeOperator as co
from PIL import Image
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
        if not vb:
            width = svg.get('width', '100%')
            height = svg.get('height', '100%')

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
        this_clip = GMImage(os.path.join(self.clips_dir, 'clip-%s.png' %
            clips[0]))
        this_clip.write(os.path.join(self.clips_dir, "clip-co-%s.png" %
            clips[0]))
        #self.masks.append(os.path.join(self.clips_dir, 'clip-co-%s.png' %
            #clips[0]))

        clip_i = 0
        for clip_id in clips[1:]:
            previous_clip = GMImage(os.path.join(self.clips_dir, 'clip-%s.png' %
                clips[clip_i]))
            this_clip = GMImage(os.path.join(self.clips_dir, 'clip-%s.png' %
                clip_id))

            this_clip.composite(previous_clip, 0, 0, co.XorCompositeOp)
            img_file = os.path.join(self.clips_dir, "clip-co-%s.png" % clip_id)
            this_clip.write(img_file)
            clip_i = clip_i + 1
            im = Image.open(img_file)
            if not im.getbbox(): # nothing there so delete it
                os.unlink(img_file)

    def _in_composite(self, previous_clips, clips):
        for prev_clip_id in previous_clips:
            for this_clip_id in clips:
                previous_clip = GMImage(os.path.join(self.clips_dir, 'clip-co-%s.png' %
                    prev_clip_id))
                this_clip = GMImage(os.path.join(self.clips_dir, 'clip-co-%s.png' %
                    this_clip_id))

                this_clip.composite(previous_clip, 0, 0, co.InCompositeOp)
                img_file = os.path.join(self.clips_dir, "clip-in-%s-%s.png" %
                    (prev_clip_id, this_clip_id))
                this_clip.write(img_file)

                im = Image.open(img_file)
                if not im.getbbox(): # nothing there so delete it
                    os.unlink(img_file)
                else:
                    self.masks.append(img_file)



class Scissors(object):
    """
    Cuts up images based on the clips.
    """
    junk_dir = 'junk' # holds untrimmed pieces
    raster_dir = 'raster'
    vector_dir = 'vector'

    def __init__(self, clips, image, target_directory):
        """
        Init with a clips object, image, and target directory.
        """
        self.image = image
        self.clips = clips
        self.target_directory = target_directory
        os.mkdir(os.path.join(self.target_directory, self.junk_dir))
        os.mkdir(os.path.join(self.target_directory, self.raster_dir))
        os.mkdir(os.path.join(self.target_directory, self.vector_dir))

    def cut(self):
        """
        Cut the image up in pieces. Return resulting bounding boxes.
        """
        i = 0
        self.pieces = {}
        for clip_mask in self.clips.masks:
            self._composite(clip_mask, self.image, i=i)
            i = i+1
        piece_json_file = open(os.path.join( self.target_directory, 'pieces.json'), 'w')
        json.dump(self.pieces, piece_json_file)

        return self.pieces


    def _composite(self, mask, pic, i=0):
        """
        composite of mask and pic. also trims it and renames with offset.
        """
        base = GMImage(pic)
        layer = GMImage(mask)
        base.composite(layer, 0, 0, co.CopyOpacityCompositeOp)
        finished_clip_filename = os.path.join(self.target_directory, self.junk_dir, "%s-%s.png" %
            (os.path.basename(pic), os.path.basename(mask)))
        base.write(finished_clip_filename)

        box = self._trim(finished_clip_filename,
                os.path.join(self.target_directory, self.raster_dir, "%i.png" % i))

        self._potrace(mask, i=i,
                trimmedpng=os.path.join(self.target_directory, self.raster_dir,"%i.png" % i))

        self.pieces[i] = box

    def _trim(self, img_file, save_path):
        """
        Trim down the image by removing alpha from the sides. Returns the
        bounding box that the image use to be in. Also returns a bmp.
        """
        im = Image.open(img_file)
        rgb_im = Image.new("RGBA", im.size, (0,0,0,0))
        rgb_im.paste(im, mask=im.split()[3]) #paste in just the alpha
        box = rgb_im.getbbox()
        trimmed_im = im.crop(box)
        trimmed_im.save(save_path)

        return box

    def _potrace(self, mask, i=0, trimmedpng=None):
        """
        Convert the mask into a svg file.
        """

        #TODO: convert the trimmedpng to a bmp, but not use imagemagick.
        # convert trimmed.png -alpha Extract trimmed.bmp
        #(bmp, ext) = os.path.splitext(trimmedpng)
        #trimmedbmp = "%s.bmp" % bmp
        trimmedbmp = os.path.join(self.target_directory, self.junk_dir,
                "%s.bmp" % i)
        subprocess.call(['convert', trimmedpng, '-alpha', 'Extract', '-negate',
            trimmedbmp], shell=False)

        potrace = ['potrace', trimmedbmp, '-s', '-o',
                os.path.join(self.target_directory, self.vector_dir, "%i.svg" % i)]
        subprocess.call(potrace, shell=False)

