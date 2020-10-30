class Orchard:
    """Class representing the Orchard game."""

    def __init__(self, raven_steps=6, fruit_pieces=4, basket=1, smart=False):
        """
        Initialization for the Orchard game.

        Parameters:
            raven_steps (int): number of steps the raven needs to take
                to reach the orchard
            fruit_pieces (int): initial number of fruits for each of the
                4 types
            basket (int): how many fruits the players can pick if
                basket appears on the die
            smart (bool): smart strategy if True, else random strategy
        """
        self.raven_steps = raven_steps
        self.fruit_pieces = fruit_pieces
        self.number_system = fruit_pieces + 1
        self.basket = basket
        self.smart = smart

    def to_decimal(self, state):
        """
        Translates the list of remaining
        [raven steps, apples, pears, pairs of cherries, plums]
        into the game state index n.

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
            aux += [raven % ns]
            raven //= ns

        aux = state[1:] + aux
        n = 0
        for i in range(len(aux)):
            n += aux[i] * (ns ** i)
        return n

    def to_state(self, n):
        """
        Translates the the game state index n into a list of remaining
        [raven steps, apples, pears, pairs of cherries, plums].

        Parameters:
            n (int): index of the game state

        Returns:
            state (list): list of remaining raven steps and fruits
        """
        ns = self.number_system
        state = []
        for _ in range(4):  # fruit pieces
            state += [n % ns]
            n //= ns
        state += [n]  # raven steps remain decimal
        return state[::-1]

    def raven_or_colour(self, state):
        """
        Computes transition probabilities from current game state to subsequent
        game states with either 1 raven step or 1 fruit less due to
        raven or colour appearing on the die.

        Parameters:
            state (list): current game state

        Returns:
            tp (list): list of transition probabilities: its 1st element
                represents the probability of transition to the state with 1
                raven step less, its 2nd element to the state with 1 apple less
                and so on
            p (double): probability that the next change of the game state
                will result from basket appearing on the die
        """
        # transitions are possible if there are raven steps or fruits left
        possible_transitions = [r > 0 for r in state]
        # available types of fruit
        available_fruits = sum(possible_transitions[1:])

        # this is conditional probability for each possible transition by
        # 1 raven step or 1 fruit resulting from raven or colour appearing on
        # the die (conditioned on the event that the game state changes)
        p = 1 / (available_fruits + 2)  # 2 = 1 (raven) + 1 (basket)

        # transition probabilities
        tp = [p if possible_transitions[i] else 0 for i in range(5)]

        # we have yet to consider the event when the basket appears on the die;
        # the corresponding probability p that still needs to be distributed
        # among the states to which basket can lead is passed on
        return tp, p

    def basket_recursion(self, current_state, p, fruits_to_pick, next_probs):
        """
        Compute probabilities for the game states resulting from basket
        appearing on the die.

        Parameters:
            current_state (list): current game state
            p (double): probability to be distributed among subsequent
                states
            fruits_to_pick (int): number of fruits we still can pick
            next_probs (list): probabilities of the game states on the next
                step

        Returns:
            next_probs (list): updated probabilities of the game states on the
                next step
        """

        if fruits_to_pick == 0 or max(current_state[1:]) == 0:
            next_probs[self.to_decimal(current_state)] += p

        else:
            if self.smart:
                m = max(current_state[1:])
                idx = [i for i, val in enumerate(
                    current_state[1:]) if val == m]
                # transition probabilities
                tp = [p / len(idx) if i in idx else 0 for i in range(4)]
            else:
                # possible transitions
                pt = [r > 0 for r in current_state[1:]]
                tp = [p / sum(pt) if pt[i] else 0 for i in range(4)]

            for i in range(4):
                if tp[i] > 0:
                    next_state = current_state[:]
                    next_state[i + 1] -= 1
                    next_probs = self.basket_recursion(
                        next_state, tp[i], fruits_to_pick - 1, next_probs)

        return next_probs

    def step(self, n, current_prob, next_probs):
        """
        Computes probabilities for the game states on the next step.

        Parameters:
            n (int): index of the game state
            current_prob (double): probability of the game state with index n
                on current step
            next_probs (list): probabilities of the games states on the next
                step

        Returns:
            next_probs (list): updated probabilities of the game states on the
                next step
        """
        current_state = self.to_state(n)
        # if the state is final
        if current_state[0] == 0 or max(current_state[1:]) == 0:
            next_probs[n] += current_prob

        else:
            # tp - transitions from current game state to game states with
            # either 1 raven step or 1 fruit less
            # bp - probability that transition from current game state results
            # from basket appearing on the die
            tp, bp = self.raven_or_colour(current_state)

            for i in range(len(tp)):
                if tp[i] > 0:
                    next_state = current_state[:]
                    next_state[i] -= 1
                    next_probs[self.to_decimal(next_state)] += \
                        current_prob * tp[i]

            # contributions of transitions resulting from basket appearing on
            # the die; current_prob * bp = probability that we are in the state
            # current_state and that the next change of the game state results
            # from basket
            next_probs = self.basket_recursion(
                current_state, current_prob * bp, self.basket, next_probs)

        return next_probs

    def play(self):
        """
        Computes the probability of the players winning the game.

        Returns:
            players_win (double): probability that the players win
        """
        # number of all possible game states
        all_states = (self.raven_steps + 1) * (self.fruit_pieces + 1) ** 4
        current_probabilities = all_states * [0]

        # initial setup
        initial_state = [self.raven_steps] + 4 * [self.fruit_pieces]
        current_probabilities[self.to_decimal(initial_state)] = 1

        # maximum number of state transitions in a game
        max_game_length = self.raven_steps + 4 * self.fruit_pieces - 1
        for _ in range(max_game_length):
            next_probabilities = all_states * [0]
            for n in range(all_states):
                if current_probabilities[n] > 0:
                    next_probabilities = self.step(
                        n, current_probabilities[n], next_probabilities)
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
