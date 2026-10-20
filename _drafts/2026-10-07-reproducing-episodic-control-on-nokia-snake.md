---
layout: post
title:  "Reproducing Episodic Control Papers' Results on Snake"
date:   2026-10-07 12:00:00 +0100
categories: blog research reinforcement-learning 
short_intro: ""
highlights:
    - Will fill later 
---

## A bit of history before

For much of my friends that know me since Tech High School, they know that 
I started doing research in Artificial Intelligence back in 2010. I joined the 
LSI (Intellgent Systems Lab) to work in project _Artífice_. And I worked in this 
project for most of my life until 2017, when I finally presented the Undergrad
Conclusion Work on a Actor-based implementation of the intelligent architecture,
which my advisor and I baptized [dl2l](/projects/#dl2l) (_d_ for distributed, _l2l_ is the acronym for 
_learn to live, live to learn_). 

After that work I was sincerely tired of that project. I felt I gave my contribution
and could take on other stuff. I went to learn other stuff, but the theme of 
artificial creatures never got out of my mind. I kept stumbling in books such as
_A Brief History Of Intelligence: Why The Evolution Of The Brain Holds The Key To The Future Of Ai_
by Max Bennet, the classic _Godel, Escher, Bach: An Eternal Golden Braid_ by Douglas Hofstadter,
and papers like [A call for embodied AI]({% post_url 2024-06-24-review-a-call-for-embodied-ia %}),
and more recently [A Path Towards Autonomous Machine Intelligence]({% post_url
2026-04-01-a-path-towards-autonomous-machine-intelligence-reviewed %}) from Yann LeCun.
That one paper describes essentially everything I did in my entire research project
up until the world model. In fact, LeCun's fundamental construct is the 
Neural Networks (NN), which I actually never applied. But the paper left me curious.
I was curious until I realized that I could use the agentic code patterns I had
in my workplace to actually do research. 

And this story is basically me and my friend Claude Code trying to answer 
scientific questions with a minimal rigour.

## Model-based versus model-free control 
The last paper I mentioned is basically about how an agent selects which action
to perform in an environment. 
The standard approach for NN and now Large Language Models (LLMs) to learn how to 
interact in an environment is reinforcement learning. 
The technique consists in rewarding/penalizing an agent based on the actions 
that it takes, much like we do when we are training a pet to do his physiological
needs in the right place. If he does it in the living room carpet one will probably
repreend the little animal viemently, and will reward him with a treat if done 
correctly in the right place. 

If this approach of penalizing/rewarding takes a long time with animals, 
imagine with a NN, that only sees zeros and ones and have to abstract from that.
In fact, training a LLM takes weeks, even months of constantly repeating examples
until it actually learns to be useful. In the other hand, we humans can learn 
way faster, sometimes only by observing the world. 
The author argues that an agent to be data efficient, it needs to construct a 
world model, an internal representation of the environment. So it can simulate
the consequences of its own actions. This allow agents to establish plans 
and calibrate their predctions as they interact with the world. 
This is known as model-based control and mamals excel on this type of decision
mechanism due to a very big pre-frontal cortex. 

But world models are not the only way an agent learns and decide. 
Animals without a pre-frontal cortex still can act very intelligently, and 
can't do long term planning. They basically decide by mechanisms that we call
classic and operant conditioning, and by episodic memory. These mechanisms are known
as model-free control strategies. 

The theory for these models are basically described in the resumes of the three papers
I read for this study, 
[Hypocampal Contribution to Control: The Third Way]({% post_url 2026-09-28-hippocampal-contributions-to-control-the-third-way-reviewed %}),
[Model-free Episodic Control]({% post_url 2026-09-29-model-free-episodic-control-reviewed %}) and 
[Neural Episodic Control]({% post_url 2026-10-04-neural-episodic-control-reviewed %}).
I'm a very practical learner. I don't feel I learn something by reading, I have
to crack it, build it and break it. This usually takes time but today with AI
you're always one prompt away of a running peace of code. 
I definitely could be building a SaaS and trying to get rich, instead I'm prompting 
claude to generate a Snake game to reproduce the results of Episodic Control papers.

I wanted to do this because _dl2l_ has an episodic memory module in it's original
version of the architecture, that I didn't port to the Akka Actor-based version 
for the sake of finishing my conclusion work on time. I wanted to understand
the state-of-the-art of episodic control and how that apply to my particular
architecture.

## How memories are formed and how they're used in action decision 

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

## A Snake game breaks the theory, why?

{% include figure.html src="/images/snake_rl/snake_dqn.gif" height="350px" 
    caption="" %}

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

- What is happening in the embedding layer?
So the first hypothesis for the agent not learning is the embedding is not 
        We developed a method to mesure the effect of each state in the game
        into the embedding and compute the
      - tune the learning rate? we did it, didn't show any relevant result
      - adjust the network? deviate from paper architecture
      - understand embedding space? change loss function? 
    
{% include figure.html src="/images/snake_rl/06b_pca3d.html" height="650px"
   caption="The same picture in three dimensions: each dot is one of the 1,282 probe states embedded by a saved agent (seed 11, 250k steps), on its first three principal components. Blue: up is a good move; orange: it is not. Black rings: the 50 nearest probe states of the example state (black diamond). Panel titles: for states where up is good, the average share of their 50 nearest states where up is also good (chance is 39%). Drag to rotate (the three views move together), scroll to zoom, hover for details." %}

## I Can’t Believe It’s Not Better

 - What the embedding learn in pacman that is not learnable here?
{% include figure.html src="/images/snake_rl/pacman_dqn.gif" height="350px" 
    caption="" %}
    Pacman have much more frequent rewards than snake, so I tried to implement
    our own Ms Pacman, with one single board and two ghosts to test the result. 



