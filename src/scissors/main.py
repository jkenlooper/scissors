from optparse import OptionParser

if __name__ == "__main__":
  parser = OptionParser(usage="%%prog ", version=__version__, description="cut stuff")

  parser.add_option("--svgpaths", "-s",
      action="store",
      type="string",
      help="Specify the svg paths file to use for cutting the image.")

  parser.add_option("--dir",
      action="store",
      type="string",
      default='tmp',
      help="The directory to store pieces in.")

  (options, args) = parser.parse_args()

  if not args and not options.svgpaths:
      parser.error("Need to specify a svgpaths document and an image filename")

