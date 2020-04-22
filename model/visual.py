import pygame
from random import randint
from sys import exit
from model.auv import AUV
from model.neuro import Net

DEBUG = 0
MAX_SPEED = 157
MAX_SPIN = 20


def generate_gate():
    pos = randint(100, 540), randint(100, 380)
    return pos


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
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("AUV simulator")

vehicle = AUV(300, 300, 0)
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

    thrust = thrust[0][0], thrust[1][0], thrust[2][0]

    print(*thrust)
    vehicle.update(thrust[0], thrust[1], thrust[2], dt)
    vehicle.render(screen)

    pygame.display.update()
    pygame.display.flip()

    frames = pygame.time.Clock()
    frames.tick(FRAMERATE)

    if vehicle.x_abs < 0:
        vehicle.x_abs = 640
    elif vehicle.x_abs > 640:
        vehicle.x_abs = 0
    if vehicle.y_abs < 0:
        vehicle.y_abs = 480
    elif vehicle.y_abs > 480:
        vehicle.y_abs = 0

print("TOTAL TIME ", epoch)
exit(0)
