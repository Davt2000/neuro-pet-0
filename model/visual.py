import pygame
from random import randint
from sys import exit
from model.auv import AUV
from model.neuro import Net

DEBUG = 0
MAX_SPEED = 157
MAX_SPIN = 20
W, H = 1920, 1080


def generate_gate():
    pos = randint(100, W-100), randint(100, H-100)
    return pos


def simulate_thrusters(x):
    if -1 < x < -0.4:
        return -0.4
    elif -0.2 < x < 0.2:
        return 0
    elif x > 1:
        return 1
    elif x < -1:
        return -1
    else:
        return x


def insane_pilot():
    x1 = randint(-1000, 1000) / 1000
    x2 = randint(-1000, 1000) / 1000
    x3 = randint(-1000, 1000) / 1000
    return x1, x2, x3,


if DEBUG:
    pilot = Net(4, 3)
    pilot.randomize()
    pilot.save("pilot1")
else:
    pilot = Net()
    pilot.load("net2")

gate_pos = generate_gate()

FRAMERATE = 30
dt = 0.1
epoch = 0

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("AUV simulator")
pos = generate_gate()
vehicle = AUV(pos[0], pos[1], -1.55)
vehicle.render(screen)

thrust = (0.3, 0.4, 0.00)
e = pygame.event.get()


while e[0] != pygame.WINDOWEVENT_CLOSE:
    epoch += 1
    screen.fill(0)

    pygame.draw.circle(screen, 0x00FF00, gate_pos, 5)
    # thrust = pilot.run([[vehicle.seek(gate_pos)], [vehicle.seek(gate_pos)], [vehicle.seek(gate_pos)]])
    # thrust = pilot.run([[vehicle.rel_v[0][0]/MAX_SPEED], [vehicle.rel_v[1][0]/MAX_SPEED], [vehicle.seek(gate_pos)]])
    thrust = pilot.run([[vehicle.rel_v[0][0]/MAX_SPEED], [vehicle.rel_v[1][0]/MAX_SPEED],
                        [vehicle.wz/MAX_SPIN], [vehicle.seek(gate_pos)]])

    thrust = simulate_thrusters(thrust[0][0]), simulate_thrusters(thrust[1][0]), simulate_thrusters(thrust[2][0])

    print(*thrust)
    vehicle.update(thrust[0], thrust[1], thrust[2], dt)
    vehicle.render(screen)

    pygame.display.update()
    pygame.display.flip()

    frames = pygame.time.Clock()
    frames.tick(FRAMERATE)

    if vehicle.x_abs < 0:
        vehicle.x_abs = W
    elif vehicle.x_abs > W:
        vehicle.x_abs = 0
    if vehicle.y_abs < 0:
        vehicle.y_abs = H
    elif vehicle.y_abs > H:
        vehicle.y_abs = 0

print("TOTAL TIME ", epoch)
exit(0)
