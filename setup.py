from setuptools import setup, find_packages
import os

name = "scissors"
version = "0.0.0"

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name=name,
    version=version,
    author='Jake Hickenlooper',
    author_email='jake@weboftomorrow.com',
    description="Cut a picture into pieces by following svg paths",
    long_description=read('README.txt'),
    url='http://www.weboftomorrow.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Topic :: Software Development :: Build Tools',
        'Environment :: Web Environment',
        ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=[
        'setuptools',
        #'libxml',
        #'py2cairo',
        #'CairoSVG',
        'pgmagick', # relies on graphicsmagick
        'svgwrite',
        'beautifulsoup4', #works on python2.6 ?

        #'glue',
      ],
    entry_points="""
    [console_scripts]
    cut = scissors.script:cut
    rasterize = scissors.script:rasterize
    """,
)
