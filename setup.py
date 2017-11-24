
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pyconf import __version__

metadata = {
    'name': 'pyconf',
    'py_modules': ['pyconf'],
    'version': __version__,
    'author': 'Shuhei Hirata',
    'author_email': 'sh7916@gmail.com',
    'license': 'MIT',
    'url': 'https://github.com/hrtshu/pyconf',
}

setup(**metadata)
