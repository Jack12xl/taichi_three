import taichi as ti
import taichi_three as t3

ti.init(ti.cpu)

scene = t3.Scene()
model = t3.Model(t3.Mesh.from_obj('assets/monkey.obj'))
scene.add_model(model)
plane = t3.Model(t3.QuadToTri(t3.MeshGrid(2)))
scene.add_model(plane)
camera = t3.Camera()
scene.add_camera_d(camera)
camerafb = t3.FrameBuffer(camera, buffers=dict(
    img=[3, float],
    normal=[3, float],
))
ssaobuf = t3.LaplacianBlur(t3.SSAO(camerafb))
buffer = t3.ImgBinaryOp(camerafb, ssaobuf, lambda x, y: x * y)
#buffer = ssaobuf
scene.add_buffer(buffer)
light = t3.Light([0.4, -1.5, -0.8], 0.9)
scene.add_light(light)
ambient = t3.AmbientLight(0.1)
scene.add_light(ambient)

plane.L2W[None] = t3.translate(0, -1, 0) @ t3.scale(2, 2, 2)
gui = ti.GUI('SSAO', buffer.res)
while gui.running:
    gui.get_event(None)
    gui.running = not gui.is_pressed(ti.GUI.ESCAPE)
    camera.from_mouse(gui)
    scene.render()
    gui.set_image(buffer.img)
    gui.show()

