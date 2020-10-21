import random


class OrchardSimulation():
    """Class representing the simulation of the Orchard game."""

    def __init__(self, num_games, raven_steps=6, fruit_pieces=4, smart=False):
        """
        Initialization for Orchard game.

        Parameters:
            raven_steps (int): number of steps the raven needs to take
                to reach the orchard
            fruit_pieces (int): initial number of pieces for each of the
                4 sorts of fruit
            smart (bool): smart strategy if True, else random strategy
        """
        self.num_games = num_games
        self.raven_steps = raven_steps
        self.fruit_pieces = fruit_pieces
        self.smart = smart

    @staticmethod
    def flag(state):
        """
        Flags the state as intermediate or final.

        Parameters:
            state (list): game state

        Returns:
            (bool): False if the game state is final else True
        """
        return state[0] > 0 and max(state[1:]) > 0

    def throw_die(self, state):
        """
        Simulates one die throw.

        Parameters:
            state (list): game state
        """
        # 0 = raven, 1 = red, 2 = yellow, 3 = green, 4 = blue, 5 = basket
        face = random.randint(0, 6)
        if face < 5 and state[face] > 0:  # raven or fruit
            state[face] -= 1
        elif face == 5:  # basket
            if self.smart:
                idx = state[1:].index(max(state[1:])) + 1
            else:
                idx = random.choice(
                    [i for i, r in enumerate(state[1:]) if r > 0]) + 1
            state[idx] -= 1
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
            # initial setup is always the same
            state = [self.raven_steps] + 4 * [self.fruit_pieces]
            while self.flag(state):  # while the state is not final
                self.throw_die(state)
            if state[0] > 0:  # there are raven steps left
                players_win += 1
        p = players_win / niter
        se = (p * (1 - p) / (niter - 1)) ** 0.5
        return p, se
