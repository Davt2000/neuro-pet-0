from random import randint, sample, choice
from math import ceil

RADIATION = 10
fun_list = [1, 2, 3, 5, 8, 13]
signl = [-1, 1]


def crossover(dna1, dna2):
    n = len(dna1)
    number_of_affected = randint(ceil(n/5), ceil(n/2))
    number_of_affected = sample([i for i in range(n)], number_of_affected)
    for i in number_of_affected:
        dna1[i], dna2[i] = dna2[i], dna1[i]

    return dna2, dna1  # lets add more chaos!


def mutate(dna):
    chance = randint(1, 100)
    if chance > RADIATION:
        return dna

    n = choice(fun_list)
    dna_len = len(dna)

    for i in range(n):
        j = randint(0, dna_len - 1)
        sign = choice(signl)
        mod = sign*chance*RADIATION/1000
        dna[j] += mod

    return dna


def select(population):
    """
    :type population: list
    [[creature_id, score],]
    """
    population.sort(reverse=True, key=lambda item: item[1])
    population = population[:15]
    chance = sum(i[1] for i in population)

    pairs = []
    for i in range(25):
        parent_0, parent_1 = randint(0, chance), randint(0, chance)
        sum0, sum1 = 0, 0

        for j in range(0, 14):
            if parent_0 >= sum0:
                parent_0 = population[j][0]  # yay, gender equality!
                break
            else:
                sum0 += population[j][1]

        for j in range(1, 15):
            if parent_1 >= sum0:
                parent_1 = population[j][0]
                if parent_0 == parent_1:
                    parent_1 = population[j-1][0]  # fuck parthenogenesis!
                break
            else:
                sum0 += population[j][1]

        pairs.append((parent_0, parent_1))

    return pairs


def procreate(dna1, dna2):
    dna1, dna2 = crossover(dna1, dna2)
    dna1, dna2 = mutate(dna1), mutate(dna2)
    return dna1, dna2

#   connect to simulator

#   generate population

#   save its data

#   create a room for simulation
#   should be simulated in ticks, maximal time is 200% from ideal

#   start simulation

#   get scores for each instance

#   cut 35

#   count parent probability and generate 50 pairs // GAY PARENTING!!!

#   create pizduks

#   REPEAT!
