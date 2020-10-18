import random
import numpy as np


def crossover(mum, dad):
    """Implements ordered crossover"""

    size = len(mum)

    # Choose random start/end position for crossover
    alice, bob = [-1] * size, [-1] * size
    start, end = sorted([random.randrange(size) for _ in range(2)])

    # Replicate mum's sequence for alice, dad's sequence for bob
    alice_inherited = []
    bob_inherited = []
    for i in range(start, end + 1):
        alice[i] = mum[i]
        bob[i] = dad[i]
        alice_inherited.append(mum[i])
        bob_inherited.append(dad[i])

    print(alice, bob)
    # Fill the remaining position with the other parents' entries
    current_dad_position, current_mum_position = 0, 0

    fixed_pos = list(range(start, end + 1))
    i = 0
    while i < size:
        if i in fixed_pos:
            i += 1
            continue

        test_alice = alice[i]
        if test_alice == -1:  # to be filled
            dad_trait = dad[current_dad_position]
            while dad_trait in alice_inherited:
                current_dad_position += 1
                dad_trait = dad[current_dad_position]
            alice[i] = dad_trait
            alice_inherited.append(dad_trait)

        # repeat block for bob and mom
        i += 1

    return alice, bob


print('Pais: {} e {}'.format(
    [4, 9, 2, 8, 3, 1, 5, 7, 6], [6, 4, 1, 3, 7, 2, 8, 5, 9]))
print('Filhos: ', crossover(
    [4, 9, 2, 8, 3, 1, 5, 7, 6], [6, 4, 1, 3, 7, 2, 8, 5, 9]))
