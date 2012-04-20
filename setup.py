import os
import sys
from distutils.core import setup

# Don't import punchfork module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'punchfork'))
import version

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

setup(name='punchfork',
      version=version.VERSION,
      description='Punchfork API Python bindings',
      author='Punchfork, Inc.',
      author_email='api@punchfork.com',
      url='https://api.punchfork.com/',
      package_data={'punchfork' : ['../VERSION']},
      packages=['punchfork'],
      install_requires = ['requests >= 0.11.1'],
      classifiers=["Environment :: Web Environment",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",]
)
