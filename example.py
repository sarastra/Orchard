#!/usr/bin/python3

import random
from time import time

from orchard_exact import Orchard
from orchard_simulation import OrchardSimulation

if __name__ == "__main__":

    random.seed(9)

    # number of simulated games
    num_games = 10 ** 5

    # My First Orchard, random strategy
    # exact result:
    game = Orchard()
    start = time()
    players_win = game.play_all()
    end = time()
    print("My First Orchard, random:")
    print("\texact result: p = {:.4f} (took {:.2f} s)".format(
        players_win, end - start))

    # simulation
    simulation = OrchardSimulation(num_games)
    start = time()
    p, se = simulation.run()
    end = time()
    print("\tsimulation:   p = {:.4f}, SE = {:.4f} (took {:.2f} s)\n".format(
        p, se, end - start))

    # My First Orchard, smart strategy
    # exact result
    game = Orchard(smart=True)
    start = time()
    players_win = game.play_all()
    end = time()
    print("My First Orchard, smart:")
    print("\texact result: p = {:.4f} (took {:.2f} s)".format(
        players_win, end - start))

    # simulation
    simulation = OrchardSimulation(num_games, smart=True)
    start = time()
    p, se = simulation.run()
    end = time()
    print("\tsimulation:   p = {:.4f}, SE = {:.4f} (took {:.2f} s)\n".format(
        p, se, end - start))

    # Orchard, random strategy
    # exact result
    game = Orchard(raven_steps=10, fruit_pieces=10)
    start = time()
    players_win = game.play_all()
    end = time()
    print("Orchard, random:")
    print("\texact result: p = {:.4f} (took {:.2f} s)".format(
        players_win, end - start))

    # simulation
    simulation = OrchardSimulation(num_games, raven_steps=10, fruit_pieces=10)
    start = time()
    p, se = simulation.run()
    end = time()
    print("\tsimulation:   p = {:.4f}, SE = {:.4f} (took {:.2f} s)\n".format(
        p, se, end - start))

    # Orchard, smart strategy
    # exact result
    game = Orchard(raven_steps=10, fruit_pieces=10, smart=True)
    start = time()
    players_win = game.play_all()
    end = time()
    print("Orchard, smart:")
    print("\texact result: p = {:.4f} (took {:.2f} s)".format(
        players_win, end - start))

    # simulation
    simulation = OrchardSimulation(
        num_games, raven_steps=10, fruit_pieces=10, smart=True)
    start = time()
    p, se = simulation.run()
    end = time()
    print("\tsimulation:   p = {:.4f}, SE = {:.4f} (took {:.2f} s)\n".format(
        p, se, end - start))
