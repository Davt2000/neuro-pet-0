F = 150  # maximal thrust of one thruster
ro = 1000  # water density
n = 1004*10**(-6)  # water viscosity
a1 = 0.3  # size parameter for thruster placement
a2 = 0.6  # size parameter for thruster placement
a3 = 0.7  # size parameter for water resistance


class Phys:
    M = 15
    J = M*(1/12)*(2.56+0.49)

    @staticmethod
    def wat_res_force(v):
        s = a3**2 # front size
        d = s/a3  # hydraulic diameter
        out = ro**2*v**3*d*s/(2*n)
        # return out
        return 0.005*(0.1*v)**2*s/2/n

    @staticmethod
    def thrust_linear_force_x(inp1, inp2):
        out = (F*(inp1+inp2))
        return out

    @staticmethod
    def thrust_linear_force_y(inp3):
        out = F*inp3
        return out

    @staticmethod
    def thrust_angle_acc(inp1, inp2, inp3):
        out = a1*a2/(a1**2+a2**2)**0.5*F*(inp2-inp1) - a1*F*inp3
        return out


def convex_polygon_intersection(coords0, coords1):
    pass

