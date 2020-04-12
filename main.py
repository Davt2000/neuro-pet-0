from model.neuro import Net
from simulator import simulate
import multiprocessing
from GA import *

net = Net(3, 4)
population = []
for i in range(50):
    # creating a population
    # save its data
    net.randomize()
    net.save("nets/net{}".format(i))
    population.append('nets/net{}'.format(i))


dna_s = []
for i in range(500):
    population_scores_alt = dict.fromkeys(population, 0)
    # start simulation and get scores
    for k in range(10):
        try:
            with multiprocessing.Pool(processes=50) as pool:         # start 4 worker processes
                result = pool.map_async(simulate, population)  # evaluate "f(10)" asynchronously in a single process
                population_with_score = result.get(timeout=5)        # prints "100" unless your computer is *very* slow
        except multiprocessing.context.TimeoutError:
            print('forced skip', i)
            continue
        for j in range(50):
            population_scores_alt[population_with_score[j][0]] += population_with_score[j][1]

    population_with_score = list(population_scores_alt.items())
    # select best
    parents = select(population_with_score)

    # create pizduks
    dna_s = []
    for pair in parents:
        net.load(pair[0])
        dna1 = net.extract_dna()
        net.load(pair[1])
        dna2 = net.extract_dna()


        dna1, dna2 = procreate(dna1, dna2)
        dna_s.append(dna1)
        dna_s.append(dna2)

    for dna, individual in zip(dna_s, population):
        net.load(individual)
        net.insert_dna(dna)
        net.save()

    for j in range(40, 50):
        # creating a population
        # save its data
        net.randomize()
        net.save("nets/net{}".format(j))
        population.append('nets/net{}'.format(j))

    print("generation ", i, "simulated")
f = open('log', 'w')

f.writelines([str(i) + '\n' for i in dna_s])
