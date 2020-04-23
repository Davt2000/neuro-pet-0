from model.neuro import Net
from simulator import simulate
import multiprocessing
from GA import *
from time import time


def generate_pos():
    pos = randint(100, 1600 - 100), randint(100, 600 - 100)
    return pos


MULT = False

net = Net(8, 5)
population = []
for i in range(50):
    # creating a population
    # save its data
    net.randomize()
    net.save("nets/net{}".format(i))
    population.append('nets/net{}'.format(i))

#  log section
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
    for k in range(20):
        if MULT:
            try:
                with multiprocessing.Pool(processes=4) as pool:         # start 4 worker processes
                    population_with_score = pool.map(simulate, population)
                    #  population_with_score = result.get(timeout=1)
            except multiprocessing.context.TimeoutError:
                print('forced skip', i)
                continue
            for j in range(50):
                population_scores_alt[population_with_score[j][0]] += population_with_score[j][1]
        else:
            pos = generate_pos()
            for individual in population:
                score = simulate(individual, pos)
                population_scores_alt[individual] += score[1]

    population_with_score = list(population_scores_alt.items())

    # select best
    population_with_score.sort(reverse=True, key=lambda item: item[1])
    parents = select(population_with_score)
    survivors = [net.load(foo[0]) for foo in population_with_score[:5]]
    net.insert_dna(survivors[0])
    net.save("best/gen{}".format(i))

    f_log = open('generation_log', 'w')
    f_log.writelines([str(foo[0]) + ' ' + str(foo[1]) + '\n' for foo in population_with_score])
    f_log.close()

    # create pizduks
    dna_s = []
    for pair in parents:
        dna1 = net.load(pair[0])
        dna2 = net.load(pair[1])

        dna1, dna2 = procreate(dna1, dna2)
        dna_s.append(dna1)
        dna_s.append(dna2)

    for survivor, individual in zip(survivors, population[:5]):
        net.insert_dna(survivor)
        net.save(individual)

    for dna, individual in zip(dna_s, population[5:]):
        net.insert_dna(dna)
        net.save(individual)

    for j in range(45, 50):
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

    print("simulation of gen took", time() - now, "sec")
    print("generation ", i, "simulated")
