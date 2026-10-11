---
layout: post
title:  "Reproducing Episodic Control Papers' Results on Snake"
date:   2026-10-07 12:00:00 +0100
categories: blog research reinforcement-learning 
short_intro: ""
highlights:
    - Will fill later 
---

- Action selection in an environment 
  - how agents interact with their environments
    - agents perform actions that change the environment
    - the 
  - how they select actions
  - reinforcement learning
    
- Model-free and Model-based control
  - model-based is when I have an internal simulation/predictor model that gives me the ability to
  - model-free is when I have a kind of heuristic based on experience that helps 
		me decide which action I should take given the current state/perception.
  - life-forms endowed with simpler nervous systems explore a lot of model-free action selection, 
		which is explained by conditioning and simple associative-episodic memory
  - An episodic memory is an n-tuple of the observation/state/reward 
  - A complex creature can chose how to behave by resorting to its previous observaiton, 
		for that, it has to be able to compare quickly what it's observing/experience right now and find 
    similar episodes 
  - Observation is usually interpreted as a whole, not by single objects in the scene
- Episodic Control
  - Model-free episodic control (MFEC) works by storing the episodes, grouped by action, 
		keyed by the perception embedding together with their outcomes
  - A metric in the embedding space is implied
  - the algorithm pulls, for an action, the corresponding embeddings 
  - Neural Episodic Control works in a similar way, but it's a learnable version of MFEC,
    as it creates a diferentiable dictionary 
  - It applies the same concepts of dictionary lookup with knn neighbours, but with 
    a differentiable key, produced from a kernel convolution of the closest neighbours
  - With this, the 
- Reproducing the results in a snake game
  - After reading the papers, I went to claude to try to reproduce the results in a 
    smaller but similar to Atari game. 
  - The chosen game was snake, from my childhood memories of playing it on my Nokia phone
  - First version of the game had three action: turn left, right and move forward 
		and it learned directly from board state 
  - I tested it in a smaller board game, 7x7 then 10x10. NEC didn't show much improvement
		as the MFEC is best suited for frequently repeating states, that actually happen in a small snake game
  - Next step was to test it in a more complex environment then. At this time things started to break
  - NEC agents stopped learning, DQN agents overperform the NEC and MFEC at a 25x25 board, something is broken
  - So I started breaking the peaces: is it the NN architecture? The learning rates? The optimizer? 
  - Claude found out that for the NEC, the encoder output was exploding, so something wrong was happening
  - I tried to bring the code as close as possible to the paper, use the same input representation, 
		same optimizer. Happened that the cause of explosion was the magnitude of input, learning from grayscale pixels
    fixed it
  - Then I realized the agent was not learning how to steer towards food. The NEC agent was steering
   mostly by chance (40% of the time) while the DQN agent was reaching up to 60% steering rate
  - Adding more training episodes didn't fix the agent, so something else is odd. The original paper claims 
    that the NEC agent can learn how to play Ms Pac-Man well, but the games are fairly different: while 
		the snake requires the agent to identify where food is and steer towards it, Pac-Man don't.
    The player mostly collect rewards every move, it has to steer to avoid the ghosts, that gives it
    negative reward, and learn how to collect the extra points that allows it to beat the ghost.
  - What could be wrong? 
    - egocentric view? what about pacman
    - embedding learning? how to solve it? 
      - tune the learning rate? we did it, didn't show any relevant result
      - adjust the network? deviate from paper architecture
      - understand embedding space? change loss function? 
    - What the embedding learn in pacman that is not learnable here?
  







