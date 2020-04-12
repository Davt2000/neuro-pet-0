from model.auv import AUV
from model.neuro import Net
from random import randint
from math import fabs, ceil

WIDTH = 1600
HEIGHT = 900
TIME_LIMIT = 500
DEBUG = 0


def generate_pos():
    pos = randint(100, WIDTH - 100), randint(100, HEIGHT - 100)
    return pos


def get_distance(pos1, pos2):
    try:
        return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5
    except OverflowError:
        return 9999999999999999


def simulate(path):
    global WIDTH, HEIGHT, TIME_LIMIT
    dt = 0.1
    epoch = 0
    minimal_distance = 9999999999999999

    GOT_TARGET = 0
    GOT_MOVED = 0
    GOT_BORDER = 0
    TIMED_OUT = 0
    TERMINAL = 1

    pilot = Net()
    pilot.load(path)
    gate_pos = generate_pos()
    veh_pos = generate_pos()
    vehicle = AUV(veh_pos[0], veh_pos[1], 0)

    initial_distance = get_distance(veh_pos, gate_pos)

    while TERMINAL:
        epoch += 1

        target = vehicle.seek(gate_pos)
        thrust = pilot.run([[target], [target], [target]])
        thrust = thrust[0][0], thrust[1][0], thrust[2][0]
        vehicle.update(thrust[0], thrust[1], thrust[2], dt)
        veh_pos = vehicle.x_abs, vehicle.y_abs

        GOT_TARGET = fabs(vehicle.x_abs - gate_pos[0]) <= 4 and fabs(vehicle.y_abs - gate_pos[1]) <= 4
        GOT_BORDER = not (0 <= vehicle.x_abs <= WIDTH or 0 <= vehicle.y_abs <= HEIGHT)
        TIMED_OUT = epoch > TIME_LIMIT
        TERMINAL = not (GOT_TARGET or GOT_BORDER or TIMED_OUT)

        distance = get_distance(veh_pos, gate_pos)
        if distance < minimal_distance:
            minimal_distance = distance
        if not GOT_MOVED:
            GOT_MOVED = fabs(thrust[0]) + fabs(thrust[1]) + fabs(thrust[2]) > 0
            if epoch > 10:
                break

    distance_score = 4 - ceil(minimal_distance / (initial_distance + 1) * 4)

    total_score = GOT_TARGET * 5 + distance_score + GOT_MOVED * 2 - GOT_BORDER - TIMED_OUT * 3

    if DEBUG:
        if GOT_MOVED:
            print("moved: 2 pts")
        print("started at", initial_distance, "distance, minimal is",
              minimal_distance, "; score is", distance_score, 'pts')
        if GOT_TARGET:
            print("got target: 5 pts")
        if GOT_BORDER:
            print("hit the border: -1 point")
        if TIMED_OUT:
            print("out of time: -3 points")
        print()

    return path, total_score
