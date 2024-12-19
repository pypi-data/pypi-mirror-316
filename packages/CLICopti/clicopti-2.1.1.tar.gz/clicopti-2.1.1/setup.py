#!/usr/bin/env python3

#Do not run this file directly!
# This `setup.py` is to be called by pip,
# reading the pyproject.toml file!
# It's purpose is to build the C++ components.

#Inspired by https://setuptools.pypa.io/en/latest/userguide/ext_modules.html

from setuptools import Extension, setup

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

#TODO: Might be possible to run SWIG straight from here

setup(
    ext_modules=[
        Extension(
            name="CLICopti._CLICopti",
            include_dirs=['h'],
            language='c++',
            sources=["swig/CLICopti_python_wrap.cc",
                     "swig/splash.cc",
                     "src/cellBase.cpp",
                     "src/cellParams.cpp",
                     "src/structure.cpp"
                     ],
            depends=["h/cellBase.h",
                     "h/cellParams.h",
                     "h/constants.h",
                     "h/structure.h"]
            )
    ]
)
