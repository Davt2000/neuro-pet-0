from model.neuro import Net
from simulator import simulate
from GA import *
from time import time, sleep
from runpy import run_path

TRAINING_STRATEGY = 1


def generate_pos():
    pos = randint(100, 1600 - 100), randint(100, 600 - 100)
    return pos


net = Net(11, 8)
population = []
for i in range(100):
    # creating a population
    # save its data
    net.randomize()
    net.save("nets/net{}".format(i))
    population.append('nets/net{}'.format(i))

#  log section
f = open('logs/score_log', 'w')
f.write('')
f.close()
f = open('logs/score_log', 'w')
f.write('')
f.close()
f_time = open('logs/time_log', 'w')
f_time.write('')
f_time.close()

dna_s = []

for i in range(10000):
    population_scores_alt = dict.fromkeys(population, 0)
    now = time()
    # start simulation and get scores
    if TRAINING_STRATEGY == 0:
        for k in range(40):
            pos = generate_pos()
            for individual in population:
                score = simulate(individual, pos, training_mode='competitive')
                population_scores_alt[individual] += score[1]
    elif TRAINING_STRATEGY == 1:
        if i < 1000:
            for k in range(20):
                for individual in population:
                    score = simulate(individual, training_mode='exercise',
                                     path_to_ex='teacher/ex{}'.format(k))
                    population_scores_alt[individual] += score[1] * 2
        elif i < 1500:
            for k in range(20):
                for individual in population:
                    score = simulate(individual, training_mode='exercise',
                                     path_to_ex='teacher/ex{}'.format(randint(0, 19)))
                    population_scores_alt[individual] += score[1]
            pos = generate_pos()
            for k in range(20):
                pos = generate_pos()
                for individual in population:
                    score = simulate(individual, pos, training_mode='competitive')
                    population_scores_alt[individual] += score[1]
        elif i < 1500:
            for k in range(10):
                for individual in population:
                    score = simulate(individual, training_mode='exercise',
                                     path_to_ex='teacher/ex{}'.format(randint(0, 19)))
                    population_scores_alt[individual] += score[1]
            pos = generate_pos()
            for k in range(20):
                pos = generate_pos()
                for individual in population:
                    score = simulate(individual, pos, training_mode='competitive')
                    population_scores_alt[individual] += score[1]

            for k in range(10):
                for individual in population:
                    score = simulate(individual, training_mode='free')
                    population_scores_alt[individual] += score[1]

        elif i < 2000:
            for k in range(5):
                for individual in population:
                    score = simulate(individual, training_mode='exercise',
                                     path_to_ex='teacher/ex{}'.format(randint(0, 19)))
                    population_scores_alt[individual] += score[1]

            for k in range(10):
                pos = generate_pos()
                for individual in population:
                    score = simulate(individual, pos, training_mode='competitive')
                    population_scores_alt[individual] += score[1]

            for k in range(25):
                for individual in population:
                    score = simulate(individual, training_mode='free')
                    population_scores_alt[individual] += score[1]
        else:
            for k in range(5):
                pos = generate_pos()
                for individual in population:
                    score = simulate(individual, pos, training_mode='competitive')
                    population_scores_alt[individual] += score[1]

            for k in range(35):
                for individual in population:
                    score = simulate(individual, training_mode='free')
                    population_scores_alt[individual] += score[1]

    population_with_score = list(population_scores_alt.items())

    # select best
    population_with_score.sort(reverse=True, key=lambda item: item[1])
    parents = select(population_with_score)
    survivors = [net.load(foo[0]) for foo in population_with_score[:5]]
    net.insert_dna(survivors[0])
    net.save("best/gen{}".format(i))

    f_log = open('logs/generation_log', 'w')
    f_log.writelines([str(foo[0]) + ' ' + str(foo[1]) + '\n' for foo in population_with_score])
    f_log.close()

    f = open('logs/score_log', mode='a')
    f.write(str(population_with_score[0][1]) + '\n')
    f.close()

    # create kids
    dna_s = []
    for pair in parents:
        dna1 = net.load(pair[0])
        dna2 = net.load(pair[1])

        dna1, dna2 = procreate(dna1, dna2)
        dna_s.append(dna1)
        dna_s.append(dna2)

    for survivor, individual in zip(survivors, population[:10]):
        net.insert_dna(survivor)
        net.save(individual)

    for dna, individual in zip(dna_s, population[10:]):
        net.insert_dna(dna)
        net.save(individual)

    for j in range(90, 100):
        # creating a population
        # save its data
        net.randomize()
        net.save("nets/net{}".format(j))
        dna_s.append(net.extract_dna())

    f = open('logs/dna_log', 'w')
    f.writelines([str(k) + '\n' for k in dna_s])
    f.close()

    cycle = int(time() - now)

    f_time = open('logs/time_log', 'a')
    f_time.write(str(cycle) + '\n')
    f_time.close()

    print("Simulation of gen", i, "took", time() - now, "sec; Results:", population_with_score[0][1], 'points')

    if i % 50 == 0 and i > 0:
        print("Preventing throttling...")
        sleep(10 * int(time() - now))
    if i % 5 == 0:
        run_path('/home/perturabo/PycharmProjects/neuro_0/plot.py')
