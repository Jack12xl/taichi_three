from ..common import *


@ti.data_oriented
class VolumeRaster:
    def __init__(self, engine, N=32, radius=16, **extra_options):
        self.engine = engine
        self.res = self.engine.res
        self.radius = radius
        self.N = N

        self.dens = ti.field(float, (N, N, N))
        self.occup = ti.field(float, self.res)
        self.tmcup = ti.field(float, self.res)

        @ti.materialize_callback
        def init_dens():
            self.dens.fill(1)

    @ti.kernel
    def render_occup(self):
        for P in ti.grouped(self.occup):
            self.occup[P] = 0
        for I in ti.grouped(self.dens):
            bias = V(0, 0, 0)#V(ti.random(), ti.random(), ti.random())
            Pl = (I + bias) / self.N * 2 - 1
            Pv = self.engine.to_viewspace(Pl)
            P = int(self.engine.to_viewport(Pv))
            if not all(0 <= P < self.res):
                continue

            DXl = mapply_dir(self.engine.V2W[None], V(1., 0., 0.)).normalized()
            DYl = mapply_dir(self.engine.V2W[None], V(0., 1., 0.)).normalized()
            Rv = V(0., 0.)
            Rl = 2 / self.N
            Rv.x = self.engine.to_viewspace(Pl + DXl * Rl).x - Pv.x
            Rv.y = self.engine.to_viewspace(Pl + DYl * Rl).y - Pv.y
            r = Rv * self.res

            rho = self.dens[I] / self.N
            self.occup[P] += rho * r.x * r.y / self.radius

    @ti.kernel
    def blur(self, src: ti.template(), dst: ti.template(), dir: ti.template()):
        for P in ti.grouped(src):
            sum = 0.0
            cnt = 0.0
            for i in range(-self.radius, self.radius + 1):
                Q = P + U2(dir) * i
                x = 4 * i / self.radius
                fac = ti.exp(-x**2)
                sum += src[Q] * fac
                cnt += fac
            dst[P] = sum / cnt

    @ti.kernel
    def render_color(self, shader: ti.template()):
        for P in ti.grouped(self.occup):
            shader.img[P] = self.occup[P]

    def render(self, shader):
        self.render_occup()
        self.blur(self.occup, self.tmcup, 0)
        self.blur(self.tmcup, self.occup, 1)
        self.render_color(shader)
