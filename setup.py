#!/usr/bin/env python

# This file ensures the compiled Cython extensions are included in wheel packages

import os
import sys
import numpy as np
from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize

# Project directory
top = os.path.dirname(os.path.abspath(__file__))

# Include directories
include_dirs = [
    top,
    os.path.join(top, "skranger"),
    os.path.join(top, "skranger", "ranger", "src"),
    os.path.join(top, "skranger", "ranger", "src", "Forest"),
    os.path.join(top, "skranger", "ranger", "src", "Tree"),
    os.path.join(top, "skranger", "ranger", "src", "utility"),
    np.get_include(),
]

def find_pyx_files(directory, files=None):
    """Recursively find all Cython extension files."""
    if files is None:
        files = []
    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        if os.path.isfile(path) and path.endswith(".pyx"):
            files.append(path.replace(os.path.sep, ".")[:-4])
        elif os.path.isdir(path):
            find_pyx_files(path, files)
    return files

def create_extension(module_name):
    """Create a setuptools build extension for a Cython extension file."""
    path = module_name.replace(".", os.path.sep) + ".pyx"
    return Extension(
        module_name,
        sources=[path],
        include_dirs=include_dirs,
        language="c++",
        extra_compile_args=["-std=c++11", "-Wall"],
        extra_link_args=["-std=c++11", "-g"],
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
    )

ext_modules = [create_extension(name) for name in find_pyx_files("skranger")]

setup(
    name="skranger",
    version="0.8.0",
    packages=find_packages(),
    ext_modules=cythonize(
        ext_modules,
        gdb_debug=False,
        force=True,
        annotate=False,
        compiler_directives={"language_level": "3"},
    ),
    package_data={
        "skranger": ["*.so", "*.pyd", "ranger/**/*"],
    },
    include_package_data=True,
)