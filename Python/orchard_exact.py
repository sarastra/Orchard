class Orchard:
    """Class representing the Orchard game."""

    def __init__(self, raven_steps=6, fruit_pieces=4, basket=1, smart=False):
        """
        Initialization for the Orchard game.

        Parameters:
            raven_steps (int): number of steps the raven needs to take
                to reach the orchard
            fruit_pieces (int): initial number of pieces for each of the
                4 sorts of fruit
            basket (int): how many pieces of fruit the players can pick if the
                basket appears on the die
            smart (bool): smart strategy if True, else random strategy
        """
        self.raven_steps = raven_steps
        self.fruit_pieces = fruit_pieces
        self.number_system = fruit_pieces + 1
        self.basket = basket
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
        Computes transition probabilities from the current game state to
        game states with either one raven step or one fruit piece less,
        not considering the event when the basket appears on the die.

        Parameters:
            state (list): current game state

        Returns:
            tp (list): tp[i] represents the probability of the transition
                from game state
                current_state = [raven steps, apples, pears, pairs of cherries, plums]
                to game state
                next_state = current_state[:]
                next_state[i] -= 1
            bp (double): probability that the next change of the game state
                results from basket being thrown
        """
        # transitions are possible if there are raven steps or fruits left
        pt = [int(r > 0) for r in state]
        available_fruits = sum(pt[1:])  # available types of fruit

        # this is conditional probability for each possible transition by
        # one raven step or one piece of fruit (conditioned on the events that
        # the current state is state and that the game state changes)
        prob = 1 / (available_fruits + 2)  # 2 = 1 (raven) + 1 (basket)

        tp = []
        for i in range(5):
            tp.append(prob if pt[i] else 0)

        # we have yet to consider the event when the basket appears on the die;
        # the corresponding probability that yet needs to be distributed among
        # the states to which basket can lead is passed on
        return tp, prob

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
        # if the state is final
        if current_state[0] == 0 or max(current_state[1:]) == 0:
            next_probabilities[n] += current_probability

        else:
            # tp - transitions from the current game state to game states with
            # either one raven step or one fruit piece less
            # bp - probability that the next change of the game state results
            # from basket appearing on the die
            tp, bp = self.transition_probabilities(current_state)

            for i in range(len(tp)):
                if tp[i] > 0:
                    next_state = current_state[:]
                    next_state[i] -= 1
                    next_probabilities[self.to_decimal(next_state)] += \
                        current_probability * tp[i]

            # transitions resulting from basket appearing on the die;
            # current_probability * bp = probability that we are in the state
            # current_state and that the next change of the game state
            # results from basket appearing on the die
            self.basket_recursion(current_state, current_probability * bp,
                                  next_probabilities, self.basket)

        return None

    def basket_recursion(self, current_state, prob, next_probabilities,
                         fruits_to_pick):
        """
        Compute probabilities for the game states resulting from basket
        appearing on the die.

        Parameters:
            current_state (list): current game state
            prob (double): probability to be distributed among subsequent
                states
            next_probabilities (list): probabilities of the games states on
                the next step if we get there from the game state with index n
            fruits_to_pick (int): number of fruits we still can pick
        """

        # there must also be fruits left
        if fruits_to_pick == 0 or max(current_state[1:]) == 0:
            next_probabilities[self.to_decimal(
                current_state)] += prob

        else:
            # tp - probabilities for each possible transition from state
            # current_state by one piece of fruit
            tp = []  # basket transition probabilities
            if self.smart:
                m = max(current_state[1:])
                idx = [i for i, val in enumerate(
                    current_state[1:]) if val == m]
                for i in range(4):
                    tp.append(prob / len(idx) if i in idx else 0)
            else:
                # possible transitions
                pt = [int(r > 0) for r in current_state[1:]]
                for i in range(4):
                    tp.append(prob / sum(pt) if pt[i] else 0)

            for i in range(4):
                if tp[i] > 0:
                    next_state = current_state[:]
                    next_state[i + 1] -= 1
                    self.basket_recursion(
                        next_state, tp[i], next_probabilities, fruits_to_pick - 1)

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

        # maximum number of state transitions in a single game
        max_game_length = self.raven_steps + 4 * self.fruit_pieces - 1
        for _ in range(max_game_length):
            next_probabilities = all_states * [0]
            for n in range(all_states):
                if current_probabilities[n] > 0:
                    self.step(n, current_probabilities[n], next_probabilities)
            current_probabilities = next_probabilities[:]

        # computing the proportion of games which the players won
        players_win = 0
        final_state = 5 * [0]
        # there are self.raven_steps possible final states for which the
        # players win
        for r in range(1, self.raven_steps + 1):
            final_state[0] = r
            players_win += current_probabilities[self.to_decimal(final_state)]

        return players_win
