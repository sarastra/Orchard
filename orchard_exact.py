class Orchard:
    """Class representing the Orchard game."""

    def __init__(self, raven_steps=6, fruit_pieces=4, smart=False):
        """
        Initialization for Orchard game.

        Parameters:
            raven_steps (int): number of steps the raven needs to take
                to reach the orchard
            fruit_pieces (int): initial number of pieces for each of the
                4 sorts of fruit
            smart (bool): smart strategy if True, else random strategy
        """
        self.raven_steps = raven_steps
        self.fruit_pieces = fruit_pieces
        self.number_system = fruit_pieces + 1
        self.smart = smart

    def to_state(self, n):
        """
        Translates the index of the game state into a list of remaining
        [raven steps, apples, pears, pairs of cherries, plums].

        Parameters:
            n (int): index of the game state

        Returns:
            state (list): list of remaining raven steps and fruits
        """
        ns = self.number_system
        state = []
        for _ in range(4):  # fruit pieces
            state.append(n % ns)
            n //= ns
        state.append(n)  # raven steps remain decimal
        return state[::-1]

    def to_decimal(self, state):
        """
        Translates the list of remaining raven steps and fruits
        into the game state index.

        Parameters:
            state (list): list of remaining raven steps and fruits

        Returns:
            n (int): index of the game state
        """
        ns = self.number_system
        raven = state[0]
        aux = []
        # rewrite raven steps in the self.number_system
        while raven > 0:
            aux.append(raven % ns)
            raven //= ns
        aux = aux[::-1] + state[1:]
        n = 0
        for i in range(len(aux)):
            n += aux[::-1][i] * (self.number_system ** i)
        return n

    def transition_probabilities(self, state):
        """
        Computes transition probabilities from a game state.

        Parameters:
            state (list): current game state

        Returns:
            tp (list): tp[i] represents the probability of the transition
            from game state
            current_state = [raven steps, apples, pears, pairs of cherries, plums]
            into game state
            next_state = current_state[:]
            next_state[i] -= 1
        """
        pt = [int(r > 0) for r in state]  # possible transitions
        available_fruits = sum(pt[1:])
        # 2 = 1 (basket) + 1 (raven);
        # if we draw an unavailable fruit then tha game state does not change
        # (we are only interested in the changes)
        tp = [1 / (available_fruits + 2)]
        if self.smart:
            tp += self.__smart(pt, available_fruits, state)
        else:
            tp += self.__random(pt, available_fruits)
        return tp

    @staticmethod
    def __random(possible_transitions, available_fruits):
        """
        Computes transition probabilities for fruit sorts for random strategy.

        Parameters:
            possible_transitions (list): if tp[i] == 1, then the transition
            from game state
            current_state = [raven steps, apples, pears, pairs of cherries, plums]
            into game state
            next_state = current_state[:]
            next_state[i] -= 1
            is possible; if tp[i] == 0 the transition is not possible.
            available_fruits (int): number of available fruit sorts

        Returns:
            tp_fruits (list): transition probabilities for fruits
        """
        tp_fruits = []
        #  we distribute the probability of a basket equally among
        #  available fruit sorts
        fruit_prob = 1 / (available_fruits + 2) * (1 + 1 / available_fruits)
        for i in range(1, 5):
            tp_fruits.append(fruit_prob if possible_transitions[i] else 0)
        return tp_fruits

    @staticmethod
    def __smart(possible_transitions, available_fruits, state):
        """
        Computes transition probabilities for fruit sorts for smart strategy.

        Parameters:
            possible_transitions (list): if tp[i] == 1, then the transition
            from game state
            current_state = [raven steps, apples, pears, pairs of cherries, plums]
            into game state
            next_state = current_state[:]
            next_state[i] -= 1
            is possible; if tp[i] == 0 the transition is not possible.
            available_fruits (int): number of available fruit sorts

        Returns:
            tp_fruits (list): transition probabilities for fruits
        """
        tp_fruits = []
        side_prob = 1 / (available_fruits + 2)
        for i in range(1, 5):
            tp_fruits.append(side_prob if possible_transitions[i] else 0)

        #  we distribute the probability of a basket equally among
        #  fruit sorts with the most pieces left
        m = max(state[1:])
        idx = [i for i, val in enumerate(state[1:]) if val == m]
        for i in idx:
            tp_fruits[i] += 1 / len(idx) * side_prob
        return tp_fruits

    def step(self, n, current_probability, next_probabilities):
        """
        Compute probabilities for the game states on the next step.

        Parameters:
            n (int): index of the game state
            current_probability (double): probability of the game state
            with index n
            next_probabilities (list): probabilities of the games states on
            the next step if we get there from the game state with index n
        """
        current_state = self.to_state(n)
        # this characterizes end of game
        if current_state[0] == 0 or max(current_state[1:]) == 0:
            next_probabilities[n] += current_probability
        else:
            tp = self.transition_probabilities(current_state)
            for i in range(len(tp)):
                if tp[i] > 0:
                    next_state = current_state[:]
                    next_state[i] -= 1
                    next_probabilities[self.to_decimal(next_state)] += \
                        current_probability * tp[i]
        return None

    def play_all(self):
        """
        Plays all games.

        Returns:
            players_win (double): probability that the players win
        """
        # number of all possible game states
        all_states = (self.raven_steps + 1) * (self.fruit_pieces + 1) ** 4
        current_probabilities = all_states * [0]

        # initial setup is always the same
        initial_state = [self.raven_steps] + 4 * [self.fruit_pieces]
        current_probabilities[self.to_decimal(initial_state)] = 1

        # maximum number of state transitions in a game
        max_game_length = self.raven_steps + 4 * self.fruit_pieces - 1
        for _ in range(max_game_length):
            next_probabilities = all_states * [0]
            for n in range(all_states):
                if current_probabilities[n] > 0:
                    self.step(n, current_probabilities[n], next_probabilities)
            current_probabilities = next_probabilities[:]

        players_win = 0
        final_state = 5 * [0]
        # there are self.raven_steps possible final states for which the
        # players win
        for r in range(1, self.raven_steps + 1):
            final_state[0] = r
            players_win += current_probabilities[self.to_decimal(final_state)]

        return players_win
