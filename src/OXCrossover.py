import random
import numpy as np


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


print('Pais: {} e {}'.format(
    [4, 9, 2, 8, 3, 1, 5, 7, 6], [6, 4, 1, 3, 7, 2, 8, 5, 9]))
print('Filhos: ', OXcrossover(
    [4, 9, 2, 8, 3, 1, 5, 7, 6], [6, 4, 1, 3, 7, 2, 8, 5, 9]))
