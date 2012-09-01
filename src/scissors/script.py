import subprocess

def run():
    print "don't run with scissors"

def cut():
    print 'chop, chop'
    from scissors.base import Clips
    c = Clips(svgfile='drawing.svg')
    #import scissors.scratch

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
