from model.auv import AUV
from model.neuro import Net
from random import randint
from math import fabs, ceil


def generate_pos(w, h):
    pos = randint(100, w - 100), randint(100, h - 100)
    return pos


def simulate_thrusters(x):
    if x < -0.4:
        return -0.4
    elif -0.2 < x < 0.2:
        return 0
    elif x > 1:
        return 1
    else:
        return x


def get_distance(pos1, pos2):
    try:
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
    except OverflowError:
        return 9999999999999999


def simulate(path, pos=(150, 150), training_mode='free', path_to_ex=''):
    TIME_LIMIT = 500
    MAX_SPEED = 120
    MAX_SPIN = 20
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

    if training_mode == 'competitive':
        WIDTH = 1500
        HEIGHT = 1500

        gate_pos = pos
        veh_pos = WIDTH/2, HEIGHT/2
        vehicle = AUV(veh_pos[0], veh_pos[1], -1.55)

    elif training_mode == 'free':
        WIDTH = randint(210, 3000)
        HEIGHT = randint(210, 3000)

        gate_pos = generate_pos(WIDTH, HEIGHT)
        veh_pos = generate_pos(WIDTH, HEIGHT)
        vehicle = AUV(veh_pos[0], veh_pos[1], randint(-150, 150) / 100)

    elif training_mode == 'exercise':
        f = open(path_to_ex, 'r')
        exercise = [list(map(int, f.readline().split())),
                    list(map(float, f.readline().split())),
                    list(map(float, f.readline().split())),
                    list(map(int, f.readline().split()))
                    ]
        f.close()

        WIDTH, HEIGHT = exercise[0][0], exercise[0][1]
        gate_pos = exercise[3][0], exercise[3][1]
        veh_pos = exercise[1][0], exercise[1][1]
        vehicle = AUV(veh_pos[0], veh_pos[1], exercise[1][2])
        vehicle.v[0][0], vehicle.v[1][0] = exercise[2][0], exercise[2][1]
    else:
        raise AssertionError("Invalid training mode '{}' in simulator".format(training_mode))

    initial_distance = get_distance(veh_pos, gate_pos)

    while TERMINAL:
        epoch += 1

        #  experiment 1: only angle
        #  thrust = pilot.run([[vehicle.seek(gate_pos)], [vehicle.seek(gate_pos)], [vehicle.seek(gate_pos)]])

        #  experiment 2: angle and all moment speeds
        thrust = pilot.run([[vehicle.seek(gate_pos)], [vehicle.rel_v[0][0] / MAX_SPEED],
                            [vehicle.rel_v[1][0] / MAX_SPEED], [vehicle.wz / MAX_SPIN], [vehicle.seek(gate_pos)]])

        thrust = simulate_thrusters(thrust[0][0]), simulate_thrusters(thrust[1][0]), simulate_thrusters(thrust[2][0])

        vehicle.update_new(thrust[0], thrust[1], thrust[2])
        vehicle.move(dt)
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

    return path, total_score
