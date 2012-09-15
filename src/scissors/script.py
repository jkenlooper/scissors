import subprocess
from optparse import OptionParser

from scissors.base import Clips, Scissors

def run():
    print "don't run with scissors"

def cut():
    parser = OptionParser(usage="%prog --dir path/to/dir --svg path/to/svgfile [options] path/to/image",
            description="cut an image by specifying the clips svg")

    parser.add_option("--dir", "-d",
            action="store",
            type="string",
            help="Set the directory to store the clip files in.",)
    parser.add_option("--svg", "-s",
            action="store",
            type="string",
            help="Set the svg file.",)

    #TODO: should just get the size from the image
    parser.add_option("--width",
            action="store",
            type="int",
            default=1280,
            help="width of image ",)
    parser.add_option("--height",
            action="store",
            type="int",
            default=960,
            help="height of image ",)

    (options, args) = parser.parse_args()

    if not args and not (options.dir and options.svg):
        parser.error("Must set a directory and svg file with an image")

    print 'snip, snip'
    mydir = options.dir
    clips = Clips(svgfile=options.svg,
                clips_dir=mydir,
                size=(options.width, options.height))

    #TODO: could probably use the scissors on multiple images
    scissors = Scissors(clips, args[0], mydir)
    scissors.cut()

#TODO: deprecated
def rasterize(svg_file_name='clip-0.svg'):
    """
    Wrapper around the batik-rasterizer
    """
    raster_cmd = ['/usr/bin/java', '-Xint', '-jar']

    #TODO: better way of getting the path to the rasterizer?
    raster_cmd.append('batik-1.7/batik-rasterizer.jar')

    raster_cmd.append(svg_file_name)

    subprocess.call(raster_cmd, shell=False)

def composite():
    """
    """
