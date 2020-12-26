import taichi as ti
import numpy as np
import tina
from glob import glob

ti.init(ti.gpu)

dens = np.load('assets/000000.npy')
scene = tina.Scene(N=dens.shape[0], taa=True, density=16)
volume = tina.SimpleVolume(N=dens.shape[0])
#model = tina.MeshModel('assets/monkey.obj')
#scene.add_object(model, tina.CookTorrance(metallic=0.8))
scene.add_object(volume)

gui = ti.GUI('volume', scene.res)

np_dirs = sorted(
    glob("E:\\Jack12\\a-toy-fluid-engine\\tmp_result\\vortex-collide-3D-256x256x256-BMcq-velRemap-1.0-8-sclrRemap-1.0-20-BlndCoeff-1.0-RBGSPS-72it-dt-0.03\\rho_npys\\*.npy")
)
print("Has {} frame".format(len(np_dirs)))
for frame, np_dir in enumerate(np_dirs):
    print("frame: ", frame)
    dens = np.load(np_dir)
    volume.set_volume_density(dens)

# while gui.running:
    scene.input(gui)
    scene.render()
    gui.set_image(scene.img)
    gui.show()
