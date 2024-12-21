# -*- coding: utf-8 -*-

import sys

extra = {}

from setuptools import setup

VERSION = "0.9.1"
classifiers = """\
Development Status :: 4 - Beta
Topic :: System :: Logging
Operating System :: POSIX
Operating System :: Microsoft :: Windows
Programming Language :: Python :: 3
Topic :: Software Development :: Libraries :: Python Modules
License :: OSI Approved :: Apache Software License
"""

setup(name='zato-ext-concurrent-log-handler',
      version=VERSION,
      author="Zato Source s.r.o.",
      py_modules=[
        "cloghandler",
        "portalocker",
        ],
      package_dir={ '' : 'src', },
      url="https://zato.io",
      license = "https://www.apache.org/licenses/LICENSE-2.0",
      description='',
      long_description='',
      platforms = [ "nt", "posix" ],
      keywords = "logging, windows, linux, unix, rotate, portalocker",
      classifiers=classifiers.splitlines(),
      zip_safe=True,
      **extra
)
