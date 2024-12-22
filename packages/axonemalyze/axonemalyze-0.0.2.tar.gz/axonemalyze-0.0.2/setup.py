import sys

sys.stderr.write(
    """
###############################################################
############### Unsupported installation method ###############
###############################################################
colav does not support installation with `python setup.py install`.
Please use `python -m pip install .` or `pip install .` instead.
"""
)
sys.exit(1)

# The below code does not execute, but Github is picky about where it finds Python packaging metadata.
# See: https://github.com/github/feedback/discussions/6456
# To be removed once GitHub catches up.
import os
from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="axonemalyze",
    author="Ammaar A. Saeed",
    author_email="ammaar_saeed@g.harvard.edu",
    description=(
        """Calculate the circularity of axoneme picks from cryo-ET images."""
    ),
    license="MIT",
    url="https://github.com/ammsa23/axonemalyze",
    long_description=read("README.md"),
    packages=find_packages(),
)
