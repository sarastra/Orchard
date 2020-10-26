import random


class OrchardSimulation():
    """Class representing the simulation of the Orchard game."""

    def __init__(self, num_games=10**5,
                 raven_steps=6, fruit_pieces=4, basket=1, smart=False):
        """
        Initialization for the Orchard game.

        Parameters:
            raven_steps (int): number of steps the raven needs to take
                to reach the orchard
            fruit_pieces (int): initial number of pieces for each of the
                four types of fruit
            basket (int): how many pieces of fruit the players can pick if the
                basket appears on the die
            smart (bool): smart strategy if True, else random strategy
        """
        self.num_games = num_games
        self.raven_steps = raven_steps
        self.fruit_pieces = fruit_pieces
        self.basket = basket
        self.smart = smart

    def throw_die(self, state):
        """
        Simulates one die roll.

        Parameters:
            state (list): game state - list of remaining
                [raven steps, apples, pears, pairs of cherries, plums]
        """
        face = random.randint(0, 6)
        # 0 = raven, 1 = apple, 2 = pear, 3 = cherries, 4 = plum, 5 = basket
        if face < 5 and state[face] > 0:  # raven or
            state[face] -= 1
        elif face == 5:  # basket
            fruits_to_pick = self.basket
            # there must also be fruits left
            while fruits_to_pick > 0 and sum(state[1:]) > 0:
                if self.smart:
                    # we take the (1st) type of fruit with the most pieces left
                    idx = state[1:].index(max(state[1:])) + 1
                else:
                    # we choose randomly among the remaining fruit types
                    idx = random.choice(
                        [i for i, r in enumerate(state[1:]) if r > 0]) + 1
                state[idx] -= 1
                fruits_to_pick -= 1
        return None

    def run(self):
        """
        Runs the simulation.

        Returns:
            p (double): proportion of games that the players won
            se (double): standard error
        """
        players_win = 0
        niter = self.num_games
        for _ in range(niter):
            # initial setup
            state = [self.raven_steps] + 4 * [self.fruit_pieces]
            # while the state is not final
            while state[0] > 0 and max(state[1:]) > 0:
                self.throw_die(state)  # simulate one die roll
            # if in the final state there are raven steps left
            if state[0] > 0:
                players_win += 1
        p = players_win / niter  # proportion of won games
        se = (p * (1 - p) / (niter - 1)) ** 0.5  # standard error of p
        return p, se
