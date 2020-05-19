from random import randint, sample, choice
from math import ceil, fabs, trunc
from model.math import seed

RADIATION = 50
fun_list = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
signl = [-1, 1]
NUMBER_OF_CHILDREN = 40
MAX_PARENTS = 20


def parent_distribution(x):
    return MAX_PARENTS - ceil((-x + 100)**0.5/10*MAX_PARENTS)


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

    dna_len = len(dna)
    n = choice(fun_list)
    while n > dna_len:
        n = choice(fun_list)

    for i in range(n):
        j = randint(0, dna_len - 1)
        while 1:
            sign = choice(signl)
            mod = sign*chance*RADIATION/1000
            if fabs(dna[j] + mod) < 1.5:
                break
            else:
                chance = randint(1, 100)
        dna[j] += mod
        dna[j] = trunc(dna[j]*1000)/1000

    chance = randint(1, 100)
    if chance > RADIATION:
        return dna

    dna[randint(0, dna_len - 1)] = seed()
    return dna


def select(population):
    """
    :type population: list
    [[creature_id, score],]
    """
    # should be sorted outside
    population = population[:MAX_PARENTS]

    pairs = []
    for i in range(NUMBER_OF_CHILDREN):
        parent_0, parent_1 = parent_distribution(randint(0, 100)),\
                             parent_distribution(randint(0, 100))
        if parent_0 > parent_1:
            parent_1, parent_0 = parent_0, parent_1

        if parent_1 == parent_0:
            if parent_0 != 0:
                parent_0 -= 1
            else:
                parent_1 += 1

        if parent_1 >= MAX_PARENTS - 1:
            if parent_1 == parent_0:
                parent_0 -= 2
            parent_1 -= 1

        parent_0, parent_1 = population[parent_0][0], population[parent_1][0]
        pairs.append((parent_0, parent_1))

    return pairs


def procreate(dna1, dna2):
    dna1, dna2 = crossover(dna1, dna2)
    dna1, dna2 = mutate(dna1), mutate(dna2)
    return dna1, dna2
