from ..common import *
from .base import VoxlEditBase


@ti.data_oriented
class VolumeTransform:
    def __init__(self, voxl):
        super().__init__(voxl)

        self.trans = ti.Matrix.field(4, 4, float, ())

        @ti.materialize_callback
        @ti.kernel
        def init_trans():
            self.trans[None] = ti.Matrix.identity(float, 4)

    @ti.func
    def get_transform(self):
        return self.trans[None] @ self.voxl.get_transform()

    def set_transform(self, trans):
        self.trans[None] = np.array(trans).tolist()
