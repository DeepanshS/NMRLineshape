import numpy
from setuptools import setup, Extension
# from distutils.core import setup
# from distutils.extension import Extension
from Cython.Distutils import build_ext
# from Cython.Build import cythonize
from os import path

from Cython.Compiler import Options

Options.docstrings = True


from os import listdir
from os.path import isfile, join


library_name = "NMRLineshape"

include_directories = ["./NMRinteraction/include"]
include_directories.append(numpy.get_include())


source_files = []

source_file_dir = ['NMRinteraction/NuclearShielding/',
                   'NMRinteraction/base_c/',
                  ]

for _dir in source_file_dir:
      for _file in listdir(_dir):
            filename = path.splitext(_file)[0]
            if _file.endswith(".c") and filename[:6] != 'cython':
                  source_files.append(_dir+_file)
            if _file.endswith(".pyx"):
                  source_files.append(_dir+_file)

print("Source files----------------------------------")
for item in source_files:
      print(item)

ext_modules = [Extension(
             name=library_name,
             sources=source_files,
            #  include_dirs=[numpy.get_include()],
            #  extra_objects= objects, # ["fc.o"],  # if you compile fc.cpp separately
             include_dirs = include_directories,  # .../site-packages/numpy/core/include
             language="c",
             # libraries=
             extra_compile_args = "-flax-vector-conversions -g".split(),
             extra_link_args = "-g".split()
             )]

setup(
      name = library_name,
      cmdclass = {'build_ext': build_ext},
      ext_modules = ext_modules,
      # ext_modules = cythonize(ext_modules)  ? not in 0.14.1
      version = '0.0.1a0',
      description = 'NMR lineshape simulator',
      author = 'Deepansh Srivastava',
      author_email= 'srivastava.89@osu.edu'
      )
