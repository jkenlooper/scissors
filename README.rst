Scissors
========

Cuts an image up into multiple pieces without losing any pixels in the process.
This is done by compositing multiple masks generated from a specially setup svg
file.  

Installing
----------

Depends on:

* batik-1.7/batik-rasterizer.jar (see the buildout.cfg which installs it)
* graphicsmagick
* potrace
  
Other python dependencies include:

* lxml
* pgmagick
* svgwrite
* beautifulsouup4
* pillow


Installing with buildout is easiest after getting a bootstrap.py file.

python2.7 path/to/bootstrap.py

./bin/buildout

Usage
-----

After installing, a 'cut' script will be in the bin directory.  Running that
will show some help.  It basically needs a path to a directory to store the
generated files, a svg file setup in a specific way, and the path to an image.

The svg editor I used to create the svg file: https://code.google.com/p/svg-edit/

Here is an example of a single cut around a llama
http://en.wikipedia.org/wiki/File:Llama_lying_down.jpg :


::

  <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink">
    <!-- Created with SVG-edit - http://svg-edit.googlecode.com/ -->
    <!-- hand edited to work with scissors -->

    <g> <!-- First Layer -->
      <g> <!-- First Group -->
        <path stroke-opacity="0" id="svg_6" d="m97.5,30c-3.5,2 -4.5,9
        0,11.5c4.5,2.5 -9,11 -9.5,17.5c-0.5,6.5 -2.5,13 1,14c3.5,1 12,3.5
        13,3c1,-0.5 -25,62.5 -16,80.5c9,18 -59,10.5 -62,19.5c-3,9 -1,11
        7,13c8,2 31.5,-7 37.5,-5.5c6,1.5 35.5,7.5 40,6c4.5,-1.5 104.5,-3
        108,-7.5c3.5,-4.5 25,4 41.5,1.5c16.5,-2.5 25,-14.5 24,-23.5c-1,-9
        -31.5,-54 -39.5,-53.5c-8,0.5 -46,5 -56.5,6.5c-10.5,1.5 -42,0
        -43,-7c-1,-7 -0.5,-44.5 -5.5,-53.5c-5,-9 -19,-26 -24,-24c-5,2 -5,6.5
        -7.5,2.5c-2.5,-4 -8.5,-1 -8.5,-1z" stroke="#000000" fill="#000000"/>
      </g>
    </g>
  </svg>


Example of the command to cut it out:
``./bin/cut --dir llama --svg Llama-simple_cut.svg --width=300 --height=200 Llama_lying_down.jpg``

Which isn't all that exciting.  But, if the llama should be cut in half then I
add another layer with two groups inside.  Note that the second group overlaps
the first group.

::

  <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
    <!-- Created with SVG-edit - http://svg-edit.googlecode.com/ -->
    <!-- hand edited to work with scissors -->

    <g> <!-- Layer 1 -->
      <g> <!-- Group 1 -->
        <path stroke-opacity="0" id="svg_6" d="m97.5,30c-3.5,2 -4.5,9
        0,11.5c4.5,2.5 -9,11 -9.5,17.5c-0.5,6.5 -2.5,13 1,14c3.5,1 12,3.5
        13,3c1,-0.5 -25,62.5 -16,80.5c9,18 -59,10.5 -62,19.5c-3,9 -1,11
        7,13c8,2 31.5,-7 37.5,-5.5c6,1.5 35.5,7.5 40,6c4.5,-1.5 104.5,-3
        108,-7.5c3.5,-4.5 25,4 41.5,1.5c16.5,-2.5 25,-14.5 24,-23.5c-1,-9
        -31.5,-54 -39.5,-53.5c-8,0.5 -46,5 -56.5,6.5c-10.5,1.5 -42,0
        -43,-7c-1,-7 -0.5,-44.5 -5.5,-53.5c-5,-9 -19,-26 -24,-24c-5,2 -5,6.5
        -7.5,2.5c-2.5,-4 -8.5,-1 -8.5,-1z" stroke="#000000" fill="#000000"/>
      </g>
    </g>

    <g> <!-- Layer 2 -->
      <g> <!-- Group 1 -->
        <path id="svg_7" d="m89,7.5l67,20.5l6,70.5l-4.5,99l-148,-1l79.5,-189z"
        stroke-opacity="0" stroke="#000000" fill="#000000"/>
      </g>
      <g> <!-- Group 2 -->
        <path id="svg_8"
        d="m74.5,-8.5l181,67l37,109l-27.5,37l-270.5,-5.5l80,-207.5z"
        stroke-opacity="0" stroke="#000000" fill="#000000"/>
      </g>
    </g>
  </svg>


Okay, so that isn't very exciting.  Obviously this is really just designed to
cut up images for use as jigsaw puzzle pieces.  It could handle other things,
but it gets complicated and I don't think I built the code to handle much else
then that. See the test.py for more examples.
