suppressMessages(library(docstring))

# number of steps the raven needs to take to reach the orchard
initial.raven.steps <- 6
# initial number of fruits for each of the 4 types
initial.fruit.pieces <- 4
# how many fruits the players can pick if basket appears on the die
basket <- 1
# playing strategy
smart.strategy <- TRUE


to.decimal <- function(state) {
  #' State to decimal
  #'
  #' Translates the list of remaining
  #' [raven steps, apples, pears, pairs of cherries, plums]
  #' into the game state index n.
  #'
  #' @param state vector of remaining raven steps and fruits
  #'
  #' @return index of the game state
  
  number.system <- initial.fruit.pieces + 1
  
  aux <- c()
  raven.steps <- state[1]
  # we will first rewrite raven steps in the number.system
  while (raven.steps > 0) {
    aux <- c(aux, raven.steps %% number.system)
    raven.steps <- raven.steps %/% number.system
  }
  aux <- c(state[5:2], aux)
  
  n <- 0
  for (i in 1:length(aux)) {
    n <- n + aux[i] * (number.system ** (i - 1))
  }
  return(n)
}


to.state <- function(n) {
  #' Decimal to state
  #'
  #' Translates the game state index n into a list of remaining
  #' [raven steps, apples, pears, pairs of cherries, plums].
  #'
  #' @param n index of the game state
  #'
  #' @return vector of remaining raven steps and fruits
  
  number.system <- initial.fruit.pieces + 1
  state <- rep(NA, 5)
  for (i in 5:2) {
    state[i] <- n %% number.system
    n <- n %/% number.system
  }
  state[1] <- n
  return(state)
}


raven.or.colour <- function(state) {
  #' Transitions due to raven or colour
  #'
  #' Computes transition probabilities from current game state to subsequent
  #' game states with either 1 raven step or 1 fruit less due to raven or colour
  #' appearing on the die.
  #'
  #' @param state current game state
  #'
  #' @return vector of transition probabilities: its 1st element represents the
  #' probability of transition to the state with 1 raven step less, its 2nd
  #' element to the state with 1 apple less and so on
  
  # transitions are possible if there are raven steps or fruits left
  possible.transitions <- state > 0
  # number of available types of fruit
  available.types <- sum(possible.transitions[2:5])
  # this is conditional probability for each possible transition by 1 raven step
  # or 1 fruit resulting from raven or colour appearing on the die (conditioned
  # on the event that the game state changes)
  p <- 1 / (available.types + 2)  # 2 = 1 (raven) + 1 (basket)
  
  tp <- rep(0, 5)  # transition probabilities
  idx <- which(possible.transitions)
  tp[idx] <- p
  return(tp)
}


basket.recursion <-
  function(current.state,
           p,
           fruits.to.pick,
           next.probs) {
    #' Transitions due to basket
    #'
    #' Computes probabilities for the game states resulting from basket
    #' appearing on the die.
    #'
    #' @param current.state current game state
    #' @param p probability to be distributed among subsequent states
    #' @param fruits.to.pick number of fruits we still can pick
    #' @param next.probs probabilities of the game states on the next step
    #'
    #' @return updated probabilities of the game states on the next step
    
    if (fruits.to.pick == 0 || max(current.state[2:5]) == 0) {
      idx <- to.decimal(current.state)
      next.probs[idx] <-  next.probs[idx] + p
    } else {
      tp = rep(0, 4)  # transition probabilities
      
      # smart strategy
      if (smart.strategy) {
        m <- max(current.state[2:5])
        idx <- which(current.state[2:5] == m)
        tp[idx] <-  p / length(idx)
      } else {
        # random strategy
        possible.transitions <- current.state[2:5] > 0
        tp <- rep(0, 4)
        tp[possible.transitions] <- p / sum(possible.transitions)
      }
      
      # calculate (intermediate) probabilities
      for (i in 1:4) {
        if (tp[i] > 0) {
          next.state <- current.state
          next.state[i + 1] <- next.state[i + 1] - 1
          next.probs <-
            basket.recursion(next.state, tp[i], fruits.to.pick - 1, next.probs)
        }
      }
      
    }
    return(next.probs)
  }


one.step <- function(n, current.prob, next.probs) {
  #' Probabilities on the next step
  #'
  #' Computes probabilities for the game states on the next step.
  #'
  #' @param n index of the game state
  #' @param current.prob probability of the game state with index n on current
  #' step
  #' @param next.probs probabilities of the game states on the next step
  #'
  #' @return updated probabilities of the game states on the next step
  
  current.state <- to.state(n)
  
  # if the state is not final
  if (current.state[1] == 0 || max(current.state[2:5]) == 0) {
    next.probs[n] <- next.probs[n] + current.prob
  } else {
    # transitions from current game state to game states with either 1 raven
    # step or 1 fruit less
    tp = raven.or.colour(current.state)
    # probability that transition from current game state results from basket
    # appearing on the die
    bp = max(tp)
    
    for (i in 1:5) {
      if (tp[i] > 0) {
        next.state <- current.state
        next.state[i] <- next.state[i] - 1
        idx <- to.decimal(next.state)
        next.probs[idx] <-  next.probs[idx] + current.prob * tp[i]
      }
    }
    
    # contributions of transitions resulting from basket appearing on the die;
    # current.prob * bp = probability that we are in the state current.state and
    # that the next change of the game state results from basket
    next.probs <-
      basket.recursion(current.state, current.prob * bp, basket, next.probs)
  }
  
  return(next.probs)
}


play <- function() {
  #' Probability of winning
  #'
  #' Computes the probability of the players winning the game
  #'
  #' @return probability that the players win
  
  # number of all possible game states
  num.all.states <-
    (initial.raven.steps + 1) * (initial.fruit.pieces + 1) ** 4 - 1
  current.probs <- rep(0, num.all.states)
  
  # initial setup
  initial.state <-
    c(initial.raven.steps, rep(initial.fruit.pieces, 4))
  current.probs[to.decimal(initial.state)] <- 1
  
  # maximum number of state transitions in a game
  max.game.length <-
    initial.raven.steps + 4 * initial.fruit.pieces - 1
  for (game.step in 1:max.game.length) {
    next.probs <- rep(0, num.all.states)
    
    for (n in 1:num.all.states) {
      if (current.probs[n] > 0) {
        next.probs <- one.step(n, current.probs[n], next.probs)
      }
    }
    current.probs <- next.probs
  }
  
  # computing the proportion of games which the players won
  players.win <- 0
  final.state <- rep(0, 5)
  # there are initial.raven.steps possible final states for which the players
  # win
  for (r in 1:initial.raven.steps) {
    final.state[1] <- r
    players.win <-
      players.win + current.probs[to.decimal(final.state)]
  }
  return(players.win)
}

# run the computations
start <- Sys.time()
play()
end <- Sys.time()
end - start
