"""""" # start delvewheel patch
def _delvewheel_patch_1_9_0():
    import os
    if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'roughpy.libs'))):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_9_0()
del _delvewheel_patch_1_9_0
# end delvewheel patch

import importlib.metadata as _ilm
import os
import platform

from pathlib import Path as _Path

try:
    __version__ = _ilm.version("RoughPy")
except _ilm.PackageNotFoundError:
    __version__ = "0.0.0"


def _add_dynload_location(path: _Path):
    if platform.system() == "Windows":
        os.add_dll_directory(str(path))
        return


if platform.system() == "Windows":
    LIBS_DIR = _Path(__file__).parent.parent / "roughpy.libs"
    if LIBS_DIR.exists():
        os.add_dll_directory(str(LIBS_DIR))

try:
    iomp = _ilm.distribution("intel-openmp")
    libs = [f for f in iomp.files if f.name.startswith("libiomp5")]
    if libs:
        _add_dynload_location(libs[0].locate().resolve().parent)
    del iomp
    del libs
except _ilm.PackageNotFoundError:
    pass

import roughpy._roughpy
from roughpy._roughpy import *

from . import tensor_functions

