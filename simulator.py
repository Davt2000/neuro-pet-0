from model.auv import AUV
from model.neuro import Net
from random import randint
from math import fabs, ceil

WIDTH = 1600
HEIGHT = 900
TIME_LIMIT = 500
DEBUG = 0
MAX_SPEED = 150
MAX_SPIN = 20


def generate_pos():
    pos = randint(100, WIDTH - 100), randint(100, HEIGHT - 100)
    return pos


def get_distance(pos1, pos2):
    try:
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
    except OverflowError:
        return 9999999999999999


def simulate(path):
    global WIDTH, HEIGHT, TIME_LIMIT
    dt = 1
    epoch = 0
    minimal_distance = 9999999999999999

    GOT_TARGET = 0
    GOT_MOVED = 0
    GOT_BORDER = 0
    TIMED_OUT = 0
    TERMINAL = 1
    GOT_DESTROYED = 0
    TIME_SCORE = 0

    pilot = Net()
    pilot.load(path)
    gate_pos = generate_pos()
    veh_pos = generate_pos()
    vehicle = AUV(veh_pos[0], veh_pos[1], 0)

    initial_distance = get_distance(veh_pos, gate_pos)

    while TERMINAL:
        epoch += 1

        #  experiment 1: only angle
        #  thrust = pilot.run([[vehicle.seek(gate_pos)], [vehicle.seek(gate_pos)], [vehicle.seek(gate_pos)]])

        #  experiment 2: angle and all moment speeds
        thrust = pilot.run([[vehicle.rel_v[0][0] / MAX_SPEED], [vehicle.rel_v[1][0] / MAX_SPEED],
                            [vehicle.wz / MAX_SPIN], [vehicle.seek(gate_pos)]])

        thrust = thrust[0][0], thrust[1][0], thrust[2][0]

        vehicle.update(thrust[0], thrust[1], thrust[2], dt)
        veh_pos = vehicle.x_abs, vehicle.y_abs

        GOT_TARGET = fabs(vehicle.x_abs - gate_pos[0]) <= 4 and fabs(vehicle.y_abs - gate_pos[1]) <= 4
        GOT_BORDER = not (0 <= vehicle.x_abs <= WIDTH or 0 <= vehicle.y_abs <= HEIGHT)
        TIMED_OUT = epoch > TIME_LIMIT
        GOT_DESTROYED = fabs(vehicle.wz) > MAX_SPIN / 1.4 or \
            fabs(thrust[0]) > 1 or fabs(thrust[1]) > 1 or fabs(thrust[2]) > 1 or \
            vehicle.spins > 20 or fabs(vehicle.get_abs_v()) > MAX_SPEED
        TERMINAL = not (GOT_TARGET or GOT_BORDER or TIMED_OUT or GOT_DESTROYED)

        distance = get_distance(veh_pos, gate_pos)
        if distance < minimal_distance:
            minimal_distance = distance
        if not GOT_MOVED:
            GOT_MOVED = fabs(thrust[0]) + fabs(thrust[1]) + fabs(thrust[2]) > 0
            if epoch > 10:
                break
        if GOT_TARGET:
            TIME_SCORE = ceil((TIME_LIMIT - epoch) / 30)

    distance_score = 9 - ceil(minimal_distance / (initial_distance + 1) * 9)

    total_score = GOT_TARGET * 10 + distance_score + GOT_MOVED * 3 - \
        GOT_BORDER * 3 - TIMED_OUT * 2 - GOT_DESTROYED * 5 + TIME_SCORE

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
