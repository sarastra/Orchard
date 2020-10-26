#!/usr/bin/python3

import csv
import random
from time import time

from orchard_exact import Orchard
from orchard_simulation import OrchardSimulation

if __name__ == "__main__":

    random.seed(0)

    # number of simulations
    num_sim = 10 ** 4

    # number of simulated games
    num_games = 10 ** 4

    # My First Orchard
    # random
    print("My First Orchard, random")
    mfo_rnd_p = []
    for sim in range(num_sim):
        simulation = OrchardSimulation(num_games)
        start = time()
        p, se = simulation.run()
        end = time()
        mfo_rnd_p.append(p)
        print("\t{} p = {:.4f}, SE = {:.4f} (took {:.2f} s)".format(
            sim, p, se, end - start))

    # My First Orchard
    # smart
    print("My First Orchard, smart")
    mfo_smt_p = []
    for sim in range(num_sim):
        simulation = OrchardSimulation(num_games, smart=True)
        start = time()
        p, se = simulation.run()
        end = time()
        mfo_smt_p.append(p)
        print("\t{} p = {:.4f}, SE = {:.4f} (took {:.2f} s)".format(
            sim, p, se, end - start))

    # Orchard
    # random
    print("Orchard, random")
    o_rnd_p = []
    for sim in range(num_sim):
        simulation = OrchardSimulation(
            num_games, raven_steps=10, fruit_pieces=10, basket=2)
        start = time()
        p, se = simulation.run()
        end = time()
        o_rnd_p.append(p)
        print("\t{} p = {:.4f}, SE = {:.4f} (took {:.2f} s)".format(
            sim, p, se, end - start))

    # Orchard
    # smart
    print("Orchard, smart")
    o_smt_p = []
    for sim in range(num_sim):
        simulation = OrchardSimulation(
            num_games, raven_steps=10, fruit_pieces=10, basket=2, smart=True)
        start = time()
        p, se = simulation.run()
        end = time()
        o_smt_p.append(p)
        print("\t{} p = {:.4f}, SE = {:.4f} (took {:.2f} s)".format(
            sim, p, se, end - start))

    with open('{}sim_{}games.csv'.format(num_sim, num_games), 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(["mfo_rnd", "mfo_smt", "o_rnd", "o_smt"])
        writer.writerows(zip(mfo_rnd_p, mfo_smt_p, o_rnd_p, o_smt_p))
