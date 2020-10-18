import numpy
import random
from scipy.spatial import distance
from itertools import permutations

cities = [
    {0: [1304, 2312]},
    {1: [3639, 1315]},
    {2: [4177, 2244]},
    {3: [3712, 1399]},
    {4: [3488, 1535]},
    {5: [3326, 1556]},
    {6: [3238, 1229]},
    {7: [4196, 1044]},
    {8: [4312, 790]},
    {9: [4386, 570]},
    {10: [3429, 1908]},
    {11: [3394, 2643]},
    {12: [2935, 3240]},
    {13: [2545, 2357]},
    {14: [2370, 2975]},
    {15: [4263, 2931]},
    {16: [2562, 1756]},
    {17: [2788, 1491]},
    {18: [2381, 1676]},
    {19: [1332, 695]},
    {20: [3715, 1678]},
    {21: [3918, 2179]},
    {22: [4061, 2370]},
    {23: [3780, 2212]},
    {24: [3676, 2578]},
    {25: [4029, 2838]},
    {26: [2507, 2376]},
    {27: [3439, 3201]},
    {28: [3140, 3550]},
    {29: [2778, 2826]},
    {30: [3007, 1970]},
]

Matrix = numpy.zeros((31, 31))


def calcEuclideanDistance(a, b):
    dist = distance.euclidean(a, b)
    return dist


def createMatrixWeight(c):
    n = len(c)
    for i in range(0, n):
        for j in range(0, n):
            if i != j:
                Matrix[i][j] = (calcEuclideanDistance(c[i][i], c[j][j]))


createMatrixWeight(cities)


def generateIndividual(cromossomeLength):
    individual = []
    while len(individual) < cromossomeLength:
        randomNumber = random.randint(0, 30)
        if randomNumber not in individual:
            individual.append(randomNumber)
    return individual


def calcFitness(ind):
    summ = 0
    start = 0
    end = len(ind)-1
    for i in range(start, end):
        #print('ind i:{} e ind i+1: {}'.format(ind[i], ind[i+1]))
        summ = summ + Matrix[ind[i]][ind[i+1]]
    #print('ind i:{} e ind i+1: {}'.format(ind[end], ind[0]))
    summ = summ + Matrix[end][ind[0]]
    return summ


def generateInitialPopulation(numberIndividuos):
    pop = []
    for i in range(0, numberIndividuos):
        ind = generateIndividual(30)
        pop.append(ind)
    return pop


def mutation(ind):
    copy_ind = ind.copy()
    print(ind)
    pointA = random.randint(0, 30)
    pointB = random.randint(0, 30)
    #print('Pontos: {} e {}'.format(pointA, pointB))

    if pointA == pointB:
        return mutation(ind)

    aux = copy_ind[pointA]
    copy_ind[pointA] = copy_ind[pointB]
    copy_ind[pointB] = aux

    fitInd = calcFitness(ind)
    fitCopy = calcFitness(copy_ind)

    if fitInd < fitCopy:
        return ind
    else:
        return copy_ind


print(mutation(generateIndividual(31)))
