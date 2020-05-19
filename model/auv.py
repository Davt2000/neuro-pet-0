from model.phys import Phys as ph
from model.math import mult
from math import sin, cos, ceil, copysign, pi, acos, fabs
from pygame.draw import polygon, circle

class AUV:
    def __init__(self, x, y, angle):
        self.wz = 0
        self.rel_a = [[0], [0]]
        self.rel_v = [[0], [0]]
        self.a = [[0], [0]]
        self.v = [[0], [0]]
        self.ez = 0
        self.x_abs = x
        self.y_abs = y
        self.angle_abs = angle
        self.prograde = ((10,), (0,))
        self.f = 1
        self.spins = 0
        self.sign = [+1, +1]
        self.log_sign = 1, 1
        self.water_res_force = 0, 0

    def rot_mat(self):
        return ((cos(self.angle_abs), -sin(self.angle_abs)),
                (sin(self.angle_abs), cos(self.angle_abs)))

    def stub_mat(self):
        return ((1, 0,),
                (0, 1,))

    def hull_pos(self):
        p_alt = (
            ((self.x_abs,), (self.y_abs,)), ((self.x_abs,), (self.y_abs,)),
            ((self.x_abs,), (self.y_abs,)), ((self.x_abs,), (self.y_abs,))
        )
        p = (
            ((-8,), (-4,)), ((+8,), (-4,)),
            ((+8,), (+3,)), ((-8,), (+3,))
        )

        p = [mult(self.rot_mat(), p[i]) for i in range(4)]

        for i in range(4):
            for j in range(2):
                p[i][j][0] = ceil(p[i][j][0] + p_alt[i][j][0])
        return p

    def calculate_thrust(self, inp1, inp2, inp3):
        self.rel_v = mult(self.rot_mat(), [[self.v[0][0]], [self.v[1][0]]])
        self.rel_a = [[ph.thrust_linear_force_x(inp1, inp2) / ph.M],
                      [ph.thrust_linear_force_y(inp3) / ph.M]]
        self.log_sign = self.sign

    def update(self, inp1, inp2, inp3):
        try:
            self.calculate_thrust(inp1, inp2, inp3)
            angle_thrust = ph.thrust_angle_acc(inp1, inp2, inp3)
            try:
                self.sign = self.wz / fabs(self.wz)

            except ZeroDivisionError:
                self.sign = 1
            self.ez = 0.1 * angle_thrust - self.sign * ph.wat_res_force(self.wz)
            self.a = mult(self.rot_mat(), self.rel_a)

        except OverflowError or ZeroDivisionError or ValueError:
            pass
        pass

    def update_new(self, inp1, inp2, inp3):
        self.calculate_thrust(inp1, inp2, inp3)
        angle_thrust = ph.thrust_angle_acc(inp1, inp2, inp3)
        self.water_res_force = -ph.wat_res_force(-(self.rel_v[0][0])) / ph.M, -ph.wat_res_force(-self.rel_v[1][0]) / ph.M
        if self.rel_v[0][0] >= 0:
            self.rel_a[0][0] += self.water_res_force[0]
        else:
            self.rel_a[0][0] -= self.water_res_force[0]
        if self.rel_v[1][0] >= 0:
            self.rel_a[1][0] += self.water_res_force[1]
        else:
            self.rel_a[1][0] -= self.water_res_force[1]
        if self.wz < 0:
            self.ez = angle_thrust + 2.5*ph.wat_res_force(-self.wz)
        else:
            self.ez = angle_thrust - 2.5*ph.wat_res_force(-self.wz)

        self.a = mult(self.rot_mat(), self.rel_a)

    def move(self, dt):
        self.v[0][0] += self.a[0][0] * dt
        self.v[1][0] += self.a[1][0] * dt
        self.x_abs += self.v[0][0] * dt
        self.y_abs += self.v[1][0] * dt

        self.wz += self.ez * dt / ph.J
        self.angle_abs += self.wz * dt
        if 2 * pi <= self.angle_abs <= 2 * pi:
            self.angle_abs /= 2 * pi
            print("360 FLIP!!!")
            self.spins += 1

        self.prograde = mult(self.rot_mat(), ((10,), (0,)))

    def seek(self, p3):
        try:
            p1 = [self.x_abs, self.y_abs]
            p2 = [self.x_abs + self.prograde[0][0], self.y_abs + self.prograde[1][0]]
            P1 = ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
            P2 = ((p3[0] - p2[0]) ** 2 + (p3[1] - p2[1]) ** 2) ** 0.5
            P3 = ((p1[0] - p3[0]) ** 2 + (p1[1] - p3[1]) ** 2) ** 0.5
            foo = (2 * P1 * P3)
        except OverflowError or ZeroDivisionError or ValueError:
            return 0

        if not foo:
            dest = 0
        else:
            try:
                dest = acos((P2 ** 2 - P1 ** 2 - P3 ** 2) / foo)
            except ValueError or ZeroDivisionError:
                dest = 0
        p3 = mult(self.rot_mat(), [[-p3[0]], [-p3[1]]])

        dest = pi - dest
        if p3[0][0] > 0:
            dest = -dest
        dest /= pi
        return dest

    def render(self, surf):
        adequate_p = self.hull_pos()
        adequate_p = [
            [adequate_p[0][0][0], adequate_p[0][1][0]],
            [adequate_p[1][0][0], adequate_p[1][1][0]],
            [adequate_p[2][0][0], adequate_p[2][1][0]],
            [adequate_p[3][0][0], adequate_p[3][1][0]],
        ]

        polygon(surf, 255, adequate_p)
        circle(surf, 0x0000aa, (ceil(self.x_abs), ceil(self.y_abs)), 3)
        circle(surf, 0xff00ff, (ceil(self.x_abs + self.prograde[0][0]), ceil(self.y_abs + self.prograde[1][0])), 3)

    def log(self):
        print("Center position {:4d} x {:4d}".format(ceil(self.x_abs), ceil(self.y_abs)))
        print("Angle (rad) ", self.angle_abs)
        print("Hull pos ", *self.hull_pos())
        print("Absolute speed ", (self.rel_v[0][0] ** 2 + self.rel_v[1][0] ** 2) ** 0.5)
        print("Rotation speed", self.wz)
        print("March and lag acceleration ", self.rel_a[0][0], self.rel_a[1][0])
        print("Angle acceleration", self.ez)
        print()

    def get_abs_v(self):
        return (self.v[0][0] ** 2 + self.v[1][0] ** 2) ** 0.5
