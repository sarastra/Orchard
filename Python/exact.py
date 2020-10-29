#!/usr/bin/python3

import csv
import random
from time import time

from orchard_exact import Orchard
from orchard_simulation import OrchardSimulation

if __name__ == "__main__":

    random.seed(0)

    # number of simulated games
    num_games = 10 ** 5

    # My First Orchard
    # random
    game = Orchard()
    start = time()
    mfo_rnd = game.play()
    end = time()
    print("My First Orchard, random:")
    print("\texact result: p = {:.5f} (took {:.2f} s)".format(
        mfo_rnd, end - start))

    # My First Orchard
    # smart
    game = Orchard(smart=True)
    start = time()
    mfo_smt = game.play()
    end = time()
    print("My First Orchard, smart:")
    print("\texact result: p = {:.5f} (took {:.2f} s)".format(
        mfo_smt, end - start))

    # Orchard
    # random
    game = Orchard(raven_steps=10, fruit_pieces=10, basket=2)
    start = time()
    o_rnd = game.play()
    end = time()
    print("Orchard, random:")
    print("\texact result: p = {:.5f} (took {:.2f} s)".format(
        o_rnd, end - start))

    # Orchard
    # smart
    game = Orchard(raven_steps=10, fruit_pieces=10, basket=2, smart=True)
    start = time()
    o_smt = game.play()
    end = time()
    print("Orchard, smart:")
    print("\texact result: p = {:.5f} (took {:.2f} s)".format(
        o_smt, end - start))

    with open('exact_results.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(["mfo_rnd", "mfo_smt", "o_rnd", "o_smt"])
        writer.writerow([mfo_rnd, mfo_smt, o_rnd, o_smt])
