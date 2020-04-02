from random import randint
from math import exp


def matrix_upgrade(f):
    def upgraded_func(x):
        if (type(x) is list) or (type(x) is tuple):
            return [upgraded_func(i) for i in x]
        else:
            return f(x)
    return upgraded_func


def mult(X, Y):
    result = [[0]*len(Y[0]) for i in range(len(X))]
    for i in range(len(X)):
        for j in range(len(Y[0])):
            for k in range(len(Y)):
                result[i][j] += X[i][k] * Y[k][j]

    return result

def seed():
    return float(randint(-1000, 1000))/1000


def sigm(x):
    return 1/(1+exp(-x))


def tanh(x):
    return 2*sigm(2*x) - 1


def relu(x):
    return max(0, x)


def myfunc(x):
    if x < 0.2:
        return 0
    else:
        return (tanh(x-0.2) + 1)/2
def eq(x):
    return x


@matrix_upgrade
def filter(x):
    if -0.1 < x < 0.1:
        return 0
    elif x > 1:
        return 1
    elif x < -0.4:
        return -0.4
    else:
        return x