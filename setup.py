#!/usr/bin/env python

import sys
from distutils.core import setup

if sys.version_info[0] < 3:
    print("Need python version >=3.0")
    exit(1)

setup(name="pyzk",
      version="0.0.2",
      description="The personal python lib of zhangkai.",
      author="Zhang Kai",
      author_email="kylerzhang11@gmail.com",
      packages=["pyzk"],
      )

