
def run():
    print "don't run with scissors"

def cut():
    print 'chop, chop'

def rasterize(svg_file_name):
    """
    Wrapper around the batik-rasterizer
    """
    raster_cmd = ['/usr/bin/java', '-Xint', '-jar']

    #TODO:
    raster_cmd.append('/path/to/batik-1.7/batik-rasterizer.jar')

    raster_cmd.append(svg_file_name)

    subprocess.call(raster_cmd, shell=False)
