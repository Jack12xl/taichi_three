import taichi_three as t3

scene = t3.Scene()
camera = t3.Camera()
scene.add_camera(camera)

light = t3.Light(dir=[-0.2, -0.6, -1.0])
scene.add_light(light)

obj = t3.Geometry.cube()
model = t3.Model(t3.Mesh.from_obj(obj))
scene.add_model(model)

gui = t3.GUI('Rotating Cube')
while gui.running:
    gui.get_event(None)
    camera.from_mouse(gui)
    model.L2W[None] = t3.rotateY(t3.get_time())
    scene.render()
    gui.set_image(camera.img)
    gui.show()