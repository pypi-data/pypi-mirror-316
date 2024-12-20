try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from codecs import open
import sys

if sys.version_info[:3] < (3, 0, 0):
    sys.stdout.write("Requires Python 3 to run.")
    sys.exit(1)

setup(
    name="autopsy",
    version="1.0.0",
    description="A new debugging experience",
    url="https://github.com/shobrook/autopsy",
    author="shobrook",
    author_email="shobrookj@gmail.com",
    keywords="debugger",
    python_requires=">=3",
)
