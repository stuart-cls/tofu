from setuptools import setup

VERSION='0.0.1'

setup(
    name='ufo-scripts',
    version=VERSION,
    author='Matthias Vogelgesang',
    author_email='matthias.vogelgesang@kit.edu',
    url='http://ufo.kit.edu',
    scripts=['bin/ufo-reconstruct'],
    long_description=open('README.md').read(),
)
