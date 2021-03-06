'''
Taichi THREE
============

Taichi THREE is an extension library of the `Taichi Programming Language <https://github.com/taichi-dev/taichi>`_, that helps rendering your 3D scenes into nice-looking 2D images to display in GUI.
'''

__version__ = (0, 0, 6)
__author__ = '彭于斌 <1931127624@qq.com>'

import taichi as ti
import taichi_glsl as ts

print(f'[Tai3D] version {".".join(map(str, __version__))}')
print(f'[Tai3D] Inputs are welcomed at https://github.com/taichi-dev/taichi_three')

from .scene import *
from .model import *
from .scatter import *
from .geometry import *
from .loader import *
from .meshgen import *
from .light import *

print(f'[Tai3D] Camera control hints: LMB to orbit, MMB to move, RMB to scale')
