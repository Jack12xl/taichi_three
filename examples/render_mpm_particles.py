import taichi as ti
import numpy as np
import tina
from glob import glob
import os

ti.init(ti.gpu)

scene = tina.Scene()

n_particle = 1024 * 128
pars = tina.SimpleParticles(n_particle)
material = tina.BlinnPhong()
scene.add_object(pars, material)

gui = ti.GUI('MPM_particles')

root_dir = "E:\Jack12\\a-toy-fluid-engine\\tmp_result\\12-30-13-06-57-MPM3D-P-131072-G-256x256x256-dt-0.004"
out_dir = os.path.join(root_dir, "rendered"+str(n_particle))
os.makedirs(out_dir, exist_ok=True)
bool_out = True

p_info_dir = sorted(glob( os.path.join(root_dir, "particle", "*.npz")))

frame_len = len(p_info_dir)
print(f"We will render {frame_len} images !")

scene.init_control(gui,
                   center=np.array([0.5, 0.0, 0.5]),
                   theta=np.pi / 2 - np.radians(30),
                   radius=1.5)

cur_frame = 0
while gui.running and cur_frame < frame_len:
    # pos = np.random.rand(1024, 3).astype(np.float32) * 2 - 1
    cur_p_info = np.load(p_info_dir[cur_frame])

    pos = cur_p_info['x']
    pars.set_particles(pos)
    # print(f"pos shape {pos.shape}")

    # color = np.random.rand(1024, 3).astype(np.float32) * 0.8 + 0.2
    color_hex = cur_p_info['c']
    # color_hex = np.ones_like(color_hex).astype(np.float32)
    # color_hex *= 1000.0
    pars.set_particle_colors_hex(color_hex)

    # radius = np.random.rand(1024).astype(np.float32) * 0.1 + 0.1
    radius = np.ones_like(color_hex).astype(np.float32)
    radius *= 0.005
    pars.set_particle_radii(radius)

    scene.input(gui)
    scene.render()
    gui.set_image(scene.img)
    gui.show(os.path.join(out_dir, f"{cur_frame:06d}.png") if bool_out else None)
    cur_frame += 1
