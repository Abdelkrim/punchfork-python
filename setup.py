import os
import sys
from distutils.core import setup

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

setup(name='punchfork',
      version='0.1',
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
