import numpy
import random
import pandas
from scipy.spatial import distance


class Individual:
    def __init__(self, cromossome, fit):
        self.cromossome = cromossome
        self.fit = fit
        self.evaluation = None

    def __repr__(self):
        return str(self.cromossome)


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


def createWeightedMatrix(c):
    n = len(c)
    for i in range(0, n):
        for j in range(0, n):
            if i != j:
                Matrix[i][j] = (calcEuclideanDistance(c[i][i], c[j][j]))


createWeightedMatrix(cities)


def generateIndividual(cromossomeLength):
    cromossome = []
    while len(cromossome) < cromossomeLength:
        randomNumber = random.randint(0, 30)
        if randomNumber not in cromossome:
            cromossome.append(randomNumber)
    fit = calcFitness(cromossome)
    return Individual(cromossome, fit)


def calcFitness(ind):
    summ = 0
    start = 0
    end = len(ind)-1
    for i in range(start, end):
        #print('ind i:{} e ind i+1: {}'.format(ind[i], ind[i+1]))
        summ = summ + Matrix[ind[i]][ind[i+1]]
    #print('ind i:{} e ind i+1: {}'.format(ind[end], ind[0]))
    summ = summ + Matrix[ind[end]][ind[0]]
    return summ


def generatePopulation(numberIndividuos):
    pop = []
    for i in range(0, numberIndividuos):
        ind = generateIndividual(31)
        pop.append(ind)
    return pop


def mutation(ind):
    copy_ind = Individual(ind.cromossome, None)
    print(ind)
    pointA = random.randint(0, 30)
    pointB = random.randint(0, 30)
    #print('Pontos: {} e {}'.format(pointA, pointB))

    if pointA == pointB:
        return mutation(ind)

    aux = copy_ind.cromossome[pointA]
    copy_ind.cromossome[pointA] = copy_ind.cromossome[pointB]
    copy_ind.cromossome[pointB] = aux

    copy_ind.fit = calcFitness(copy_ind.cromossome)

    # print(ind.fit)
    # print(copy_ind.fit)

    if ind.fit < copy_ind.fit:
        return ind
    else:
        return copy_ind


def getBestWorstFit(pop):
    b, w = 999999999999, 0
    bInd, wInd = None, None
    for ind in pop:
        if b > ind.fit:
            b = ind.fit
            bInd = ind

        if w < ind.fit:
            w = ind.fit
            wInd = ind
    return bInd, wInd


def evaluateInd(pop, Zmin, Zmax, r, m):
    for ind in pop:
        a = ind.fit - Zmin
        b = Zmax - Zmin + r
        ev = (1-(a/b)) ** m
        ind.evaluation = ev


def getTotalFitness(pop):
    totalFit = 0
    for i in pop:
        totalFit = totalFit + i.fit

    return totalFit


def getRelativeFitness(pop):
    totalfit = getTotalFitness(pop)
    relativeFitness = [f.fit/totalfit for f in pop]

    return relativeFitness


def getProbabilities(pop):
    relativeFitiness = getRelativeFitness(pop)
    probabilities = [sum(relativeFitiness[:f+1])
                     for f in range(len(relativeFitiness))]

    return probabilities


def rouleteWheel(pop, number):
    probabilities = getProbabilities(pop)
    chosen = []
    while len(chosen) < number:
        r = random.random()
        for (i, ind) in enumerate(pop):
            if r <= probabilities[i]:
                chosen.append(ind)
                break
    return chosen


def OXcrossover(a, b):
    size = len(a)

    # Choose random start/end position for crossover
    alice, bob = [-1] * size, [-1] * size
    start, end = sorted([random.randrange(size) for _ in range(2)])

    # Replicate mum's sequence for alice, dad's sequence for bob
    alice_inherited = []
    bob_inherited = []
    for i in range(start, end + 1):
        alice[i] = a[i]
        bob[i] = b[i]
        alice_inherited.append(a[i])
        bob_inherited.append(b[i])

    #print(alice, bob)
    # Fill the remaining position with the other parents' entries
    current_b_position, current_a_position = 0, 0

    fixed_pos = list(range(start, end + 1))
    i = 0
    while i < size:
        if i in fixed_pos:
            i += 1
            continue

        test_alice = alice[i]
        if test_alice == -1:  # to be filled
            b_trait = b[current_b_position]
            while b_trait in alice_inherited:
                current_b_position += 1
                b_trait = b[current_b_position]
            alice[i] = b_trait
            alice_inherited.append(b_trait)
        i += 1

    fixed_pos = list(range(start, end + 1))
    i = 0
    while i < size:
        if i in fixed_pos:
            i += 1
            continue

        test_bob = bob[i]
        if test_bob == -1:  # to be filled
            a_trait = a[current_a_position]
            while a_trait in bob_inherited:
                current_a_position += 1
                a_trait = a[current_a_position]
            bob[i] = a_trait
            bob_inherited.append(a_trait)
        i += 1

    return alice, bob


def RunGeneticAlgorithm(generations, numberOfIndividuals, crossoverProbability, mutationProbability):
    initialPopulation = generatePopulation(numberOfIndividuals)
    basePopulation = initialPopulation
    globalBestSolution = Individual(None, float('inf'))
    gen = 0

    while gen <= generations:
        print('Generation: {}'.format(gen))
        bestInd, worstInd = getBestWorstFit(basePopulation)

        #print('Best: {} and Worst: {}'.format(bestInd.fit, worstInd.fit))

        evaluateInd(basePopulation, bestInd.fit, worstInd.fit, 1, 2)

        # for i in initialPopulation:
        #    print('Fit: {}, Eval: {}'.format(i.fit, i.evaluation))

        selectedIndividuals = rouleteWheel(basePopulation, 50)

        individualsBeforeCrossover = []
        for i in range(0, len(selectedIndividuals)-1, 2):
            r = random.random()
            if r <= crossoverProbability:
                indA, indB = selectedIndividuals[i], selectedIndividuals[i+1]

                childA, childB = OXcrossover(indA.cromossome, indB.cromossome)

                indA.cromossome = childA
                indB.cromossome = childB
                individualsBeforeCrossover.append(indA)
                individualsBeforeCrossover.append(indB)

        for individual in individualsBeforeCrossover:
            r = random.random()
            if r <= mutationProbability:
                individual = mutation(individual)

        individualsBeforeMutation = individualsBeforeCrossover
        number = numberOfIndividuals - len(individualsBeforeMutation)

        moreIndividuals = generatePopulation(number)

        basePopulation = individualsBeforeMutation + moreIndividuals

        if globalBestSolution.fit > bestInd.fit:
            globalBestSolution = bestInd

        print('Best solution of generattion: ', globalBestSolution.fit)
        gen += 1

    return globalBestSolution


best = RunGeneticAlgorithm(1000, 200, 0.9, 0.02)

print('FINAL RESULTS: THE BEST SOLUTION')
print('Fit: {}'.format(best.fit))
print('Cromossome: {}'.format(best.cromossome))
