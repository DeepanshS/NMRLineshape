import numpy
from setuptools import setup, Extension
# from distutils.core import setup
# from distutils.extension import Extension
from Cython.Distutils import build_ext
# from Cython.Build import cythonize


from Cython.Compiler import Options

Options.docstrings = True


from os import listdir
from os.path import isfile, join


library_name = "NMRinteraction"
#location = '/Users/deepanshsrivastava/Library/Developer/Xcode/DerivedData/'
# object_directories = "./lib"
# object_files = [file for file in listdir(object_directories) if file.endswith(".a")]
# objects = [object_directories+file for file in object_files]

# print ('libraries included')
# print (objects)
# print ('------------------------------------------------------------------------')

include_directories = ["./NMRinteraction/NuclearShielding"]
include_directories.append(numpy.get_include())
# include_directories.append(object_directories + "include/")

print ('location of include files')
print (include_directories)
print ('------------------------------------------------------------------------')

path_to_pyx_files = library_name + " Sources Cython/"
pyx_file = [path_to_pyx_files + "c_CSA_static_lineshape.pyx"]
print ('Cython file')
print (pyx_file)
print ('------------------------------------------------------------------------')
print ()

source_file = []
source_file_dir = 'NMRinteraction/NuclearShielding/'
for _file in listdir(source_file_dir):
      if _file.endswith(".c"):
            source_file.append(source_file_dir+_file)

for item in pyx_file:
      source_file.append(item)

print (source_file)

ext_modules = [Extension(
             name=library_name,
             sources=source_file,
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
      ext_modules = ext_modules
      # ext_modules = cythonize(ext_modules)  ? not in 0.14.1
      # version=
      # description=
      # author=
      # author_email=
      )
