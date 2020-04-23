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


def get_distance(pos1, pos2):
    try:
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
    except OverflowError:
        return 9999999999999999


def simulate(path, pos):
    global WIDTH, HEIGHT, TIME_LIMIT, MAX_SPEED, MAX_SPIN
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
    SPINNED_TO_DEATH = 0

    pilot = Net()
    pilot.load(path)
    gate_pos = pos
    veh_pos = WIDTH/2, HEIGHT/2
    vehicle = AUV(veh_pos[0], veh_pos[1], -1.55)

    initial_distance = get_distance(veh_pos, gate_pos)

    while TERMINAL:
        epoch += 1

        #  experiment 1: only angle
        #  thrust = pilot.run([[vehicle.seek(gate_pos)], [vehicle.seek(gate_pos)], [vehicle.seek(gate_pos)]])

        #  experiment 2: angle and all moment speeds
        thrust = pilot.run([[vehicle.seek(gate_pos)], [vehicle.rel_v[0][0] / MAX_SPEED],
                            [vehicle.rel_v[1][0] / MAX_SPEED], [vehicle.wz / MAX_SPIN], [vehicle.seek(gate_pos)]])

        thrust = simulate_thrusters(thrust[0][0]), simulate_thrusters(thrust[1][0]), simulate_thrusters(thrust[2][0])

        vehicle.update(thrust[0], thrust[1], thrust[2], dt)
        veh_pos = vehicle.x_abs, vehicle.y_abs

        GOT_TARGET = fabs(vehicle.x_abs - gate_pos[0]) <= 4 and fabs(vehicle.y_abs - gate_pos[1]) <= 4
        GOT_BORDER = not (0 <= vehicle.x_abs <= WIDTH or 0 <= vehicle.y_abs <= HEIGHT)
        TIMED_OUT = epoch > TIME_LIMIT
        GOT_DESTROYED = fabs(vehicle.get_abs_v()) > MAX_SPEED or \
            fabs(thrust[0]) + fabs(thrust[1]) + fabs(thrust[2]) > 1.75
        SPINNED_TO_DEATH = fabs(vehicle.wz) > MAX_SPIN / 1.4 or vehicle.spins > 20
        TERMINAL = not (GOT_TARGET or GOT_BORDER or TIMED_OUT or GOT_DESTROYED or SPINNED_TO_DEATH)

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

    total_score = GOT_TARGET * 12 + distance_score + GOT_MOVED * 4 - \
        GOT_BORDER * 3 - TIMED_OUT * 2 - GOT_DESTROYED * 4 - SPINNED_TO_DEATH*7 + TIME_SCORE

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
